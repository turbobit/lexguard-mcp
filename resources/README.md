# MCP Resources (정적 인덱스)

서버는 JSON-RPC `resources/list`, `resources/read`로 법령·판례·법령해석 리소스를 제공합니다. 아래 URI 스킴은 런타임과 동일합니다.

| URI 형식 | 용도 |
|----------|------|
| `law://{법령명}` | 법령 본문 조회 (예: `law://근로기준법`) |
| `case://{검색어}` | 판례 검색 요약 (상위 5건) |
| `interpret://{검색어}` | 법령해석 검색 요약 (상위 5건) |

`resources/list`에는 대표 법령과 `resourceTemplates`가 포함됩니다.
