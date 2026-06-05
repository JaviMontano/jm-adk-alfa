# XLSX Output Template - Prompt Evaluation Matrix

## Sheet 1: Prompt Catalog

| Column | Type | Description |
|--------|------|-------------|
| A: Prompt ID | Text | PE-001, PE-002... |
| B: Name | Text | Descriptive name |
| C: Pattern | Dropdown | Zero-shot/Few-shot/Reasoning scaffold/System instruction/Meta |
| D: Target Model | Dropdown | Claude/Gemini/GPT/Llama |
| E: Prompt Text | Long text | Full prompt content |
| F: Status | Dropdown | Draft/Testing/Active/Deprecated |

## Sheet 2: Evaluation Matrix

| Column | Type | Description |
|--------|------|-------------|
| A: Prompt ID | Reference | Links to Sheet 1 |
| B: Test Input | Text | Input used for testing |
| C: Expected Output | Text | What should be produced |
| D: Actual Output | Text | What was produced |
| E: Accuracy | % | Correct? (0-100%) |
| F: Format Compliance | Boolean | Matches schema? |
| G: Token Cost | Number | Input + output tokens |
| H: Latency (ms) | Number | Response time |

## Sheet 3: Summary Dashboard

- Prompt count by pattern (pie chart)
- Average accuracy by model (bar chart)
- Token cost trend (line chart)
- Conditional formatting: red < 80%, yellow 80-90%, green > 90%

## Formatting
- Header row: Gold background #FFD700, Arial Bold
- Data rows: Alternating Navy #0A122A / Surface #1E293B
- Freeze top row and first column
