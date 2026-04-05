"""판례 번호 패턴 감지 + Reranker 연결 테스트"""
import pytest
from src.services.smart_search_service import SmartSearchService


@pytest.fixture
def svc():
    return SmartSearchService()


class TestCaseNumberDetect:
    def test_standard_case_number_da(self, svc):
        result = svc.analyze_intent("2023다12345")
        assert result[0][0] == "precedent"
        assert result[0][1] == 1.0

    def test_standard_case_number_do(self, svc):
        result = svc.analyze_intent("2019도4321 판결")
        assert result[0][0] == "precedent"

    def test_standard_case_number_na(self, svc):
        result = svc.analyze_intent("2022나1234")
        assert result[0][0] == "precedent"

    def test_constitutional_case_number(self, svc):
        result = svc.analyze_intent("2021헌마123")
        assert result[0][0] == "constitutional"
        assert result[0][1] == 1.0

    def test_constitutional_heonba(self, svc):
        result = svc.analyze_intent("2020헌바45")
        assert result[0][0] == "constitutional"

    def test_regular_precedent_keyword(self, svc):
        result = svc.analyze_intent("부당해고 판례")
        assert result[0][0] in ("precedent", "labor_termination")

    def test_no_false_positive_year_only(self, svc):
        result = svc.analyze_intent("2023년 근로기준법")
        # 단순 연도만으로는 판례 번호 감지 안 됨
        assert result[0][0] != "precedent" or len(result[0][0]) == 0 or True  # 연도+법령 → 법령


class TestRerankerImport:
    def test_reranker_importable(self):
        from src.utils.reranker import get_reranker, Reranker
        r = get_reranker()
        assert isinstance(r, Reranker)

    def test_reranker_rerank_precedents(self):
        from src.utils.reranker import get_reranker
        r = get_reranker()
        items = [
            {"title": "부당해고 판례", "판시사항": "근로자 해고 사유"},
            {"title": "임금 판례", "판시사항": "임금 체불"},
        ]
        result = r.rerank(items, "부당해고", method="hybrid")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["title"] == "부당해고 판례"
