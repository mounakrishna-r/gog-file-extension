# .gog File Format Specification

`.gog` files are YAML documents with the following structure:

## 1. meta
| Field | Type | Required |
|-------|------|----------|
| title | string | ✅ |
| author | string | ✅ |
| created | string (ISO date) | ✅ |

## 2. prompt
| audience | string | ✅ |
| tone | string (`casual`, `academic`, etc.) | ✅ |
| format | string | ✅ |
| context | string | ✅ |

## 3. render
Font, layout, style info.

## 4. content
- `generated`: bool
- `value`: string (AI-generated text)
