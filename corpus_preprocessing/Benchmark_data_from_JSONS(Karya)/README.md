For retrieving data from Karya APP (Crowd-Sourced Data) which are JSON files for each word.

### Instance:
```
{
  "language": "SA",
  "word_id": "2992839",
  "word": "वृषभस्कन्धं",
  "worker_id": "562949953421964",
  "access_code": "4992425636624693",
  "input": {},
  "output": {
    "vrushabhaskandham": {
      "origin": "HUMAN",
      "status": "VALID"
    }
  },
  "report": {
    "vrushabhaskandham": {
      "origin": "HUMAN",
      "status": "VALID"
    }
  },
  "variants": {
    "vrushabhaskandham": {
      "origin": "HUMAN",
      "status": "VALID"
    }
  },
  "max_credits": 4,
  "credits": 1
}

```

### Fields
- `language:` ISO Language Code
- `word` Native word
- `access_code` Worker codes to access the APP
- `output` Output of Transliteration phase (Transliterated by Annotator)
- `variants` Output of Validation phase (Validated by Validator) 
