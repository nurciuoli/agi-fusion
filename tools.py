#worker util jsons

post_plan = {
    "name": "post_plan",
    "description": "Use this to post your plan for everyone to see",
    "parameters": {
        "type": "object",
        "properties": {
            "objective": {"type": "string"},
            "tasks": {
                "type": "array",
                "description": "Each individual task needed to accomplish the objective",
                "items": {
                    "type": "object",
                    "properties": {
                        "details": {"type": "string"},
                        "choices": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["details"],
                },
            },
        },
        "required": ["objective", "tasks"],
    },
}



get_help = {
    "name": "get_help",
    "description": "Use this to delegate a single or multiple tasks to a team of workers. Break down the objective into as many individual steps as it makes sense",
    "parameters": {
        "type": "object",
        "properties": {
            "objective": {"type": "string"},
            "tasks": {
                "type": "array",
                "description": "An array of individual tasks to accomplish the overall objective, and an assignment",
                "items": {
                    "type": "object",
                    "properties": {
                        "instructions": {"type": "string",
                                         "description":"a detailed prompt describing exactly what the worker should do and any context needed"},
                        "worker_type": {
                            "type": "string",
                            "enum": ["SOFTWAREENGINEER", "WRITER"],
                        },
                        "choices": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["instructions","worker_type"],
                },
            },
        },
        "required": ["objective", "tasks"],
    },
}

instruct_help = {
    "name": "instruct_help",
    "description": "Use this to delegate a task, they will have no context so provide significant detail on instructions",
    "parameters": {
        "type": "object",
        "properties": {
            "instructions": {
                "type": "string",
                "description": "Standalone instructions for the project",
            },
        },
    },"required": ["instructions"],
}


file_manager = {
    "name": "file_upload",
    "description": "Use this to archive multiple files at once to the directory",
    "parameters": {
        "type": "object",
        "properties": {
            "files": {
                "type": "array",
                "description": "Standalone files for use in the project",
                "items": {
                    "type": "object",
                    "properties": {
                        "file_name_with_extension": {"type": "string",
                                      "description":"a name and filepath for the file. EXAMPLE: main.py, poem1.txt, templates/index.html"},
                        "content": {"type": "string",
                                    "description":"content to archive, such as code, text, ect"},
                                    "choices": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["file_name_with_extension","content"],
                },
            },
        },
        "required": ["files"],
    },
}