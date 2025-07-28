# Smart PDF Assistant for HR Professionals

Hey there! 👋 This is a smart tool I built to help HR professionals breeze through PDF documents. It's like having a personal assistant who knows exactly what you're looking for in those lengthy documents, especially when dealing with forms and compliance stuff.

## What's Inside

Here's how everything is organized:

```
.
├── input/                  # Drop your PDFs here
├── output/                 # Your analysis results will appear here
├── app/
│   ├── src/               # The brains of the operation
│   │   ├── main.py        # The main script
│   │   ├── simple_main.py # A streamlined version
│   │   ├── processor.py   # The document analysis magic
│   │   └── utils.py       # Helpful utilities
│   ├── tests/             # Making sure everything works
│   │   └── ... various test files
│   └── config/            # Your settings live here
│       └── persona.json   # Customize how the tool works for you
├── Dockerfile             # For Docker fans
└── requirements.txt       # What we need to run
```

## How It Works

I've built this tool to be smart about finding what matters to you. Here's the secret sauce:

1. **Smart Text Extraction**: It carefully pulls text from your PDFs, keeping the formatting intact.

2. **Section Detective**: It finds important sections in your documents, just like you would when skimming through.

3. **Relevance Magic**: Using some clever analysis, it figures out which parts are most relevant to what you're trying to do.

4. **Deep Dive**: It doesn't just stop at sections - it digs into subsections to find the exact information you need.

5. **Clean Results**: Everything is neatly packaged in a JSON file that's easy to work with.

## Getting Started

### What You'll Need

- Python 3.10 or newer
- Docker (optional, if you prefer containerization)

### Quick Setup

1. Get everything ready:
```bash
pip install -r requirements.txt
```

2. Drop your PDF files in the `input/` folder.

3. Customize `app/config/persona.json` with:
   - What you're working on (`challenge_info`)
   - Your documents list
   - Your role (e.g., "HR professional")
   - What you're trying to accomplish

4. Run it:
```bash
python app/src/main.py
```

Or try the simpler version:
```bash
python app/src/simple_main.py
```

5. Check out your results in the `output/` folder!

### Docker Setup

Prefer Docker? I've got you covered:

1. Build it:
```bash
docker build --platform linux/amd64 -t pdf-assistant .
```

2. Set up your `app/config/persona.json` and add your PDFs to `input/`.

3. Run it:
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-assistant
```

On Windows PowerShell:
```powershell
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none pdf-assistant
```

## Input Setup

Your `persona.json` should look something like this:

```json
{ 
  "challenge_info": { 
    "challenge_id": "round_1b_003", 
    "test_case_name": "create_manageable_forms", 
    "description": "Creating manageable forms" 
  }, 
  "documents": [ 
    { 
      "filename": "Learn Acrobat - Create and Convert_1.pdf", 
      "title": "Learn Acrobat - Create and Convert_1" 
    }
  ], 
  "persona": { 
    "role": "HR professional" 
  }, 
  "job_to_be_done": { 
    "task": "Create and manage fillable forms for onboarding and compliance." 
  } 
}
```

## What You Get

Your results will look like this:

```json
{
  "metadata": {
    "documents": ["onboarding_form.pdf"],
    "persona": {
      "role": "HR professional"
    },
    "job_to_be_done": {
      "task": "Create and manage fillable forms for onboarding and compliance."
    },
    "challenge_info": {
      "challenge_id": "round_1b_003",
      "test_case_name": "create_manageable_forms",
      "description": "Creating manageable forms"
    },
    "timestamp": "2024-01-20T14:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "onboarding_form.pdf",
      "page": 3,
      "section_title": "Creating Fillable Forms",
      "importance_rank": 1,
      "relevance_score": 0.92
    }
  ],
  "sub_section_analysis": [
    {
      "document": "onboarding_form.pdf",
      "refined_text": "Here's how to create a fillable form: Start by selecting Tools > Forms > Create...",
      "page": 3
    }
  ]
}
```

Hope this helps make your document processing a bit easier! Let me know if you need any help getting started. 😊