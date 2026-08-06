import os
import json

template_path = 'Week 2 - System Design and Memory/Week_2_Quiz.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

def create_quiz(week_num, week_dir, topic, questions):
    content = template.replace('Week 2 Quiz: System Design and Networking', f'Week {week_num} Quiz: {topic}')
    content = content.replace('Week 2 Quiz</h1>', f'Week {week_num} Quiz</h1>')
    content = content.replace('Test your understanding of System Design and Networking', f'Test your understanding of {topic}')
    content = content.replace('Week_2_Student_Notes.html', f'Week_{week_num}_Student_Notes.html')
    
    start_str = "const questions = ["
    end_str = "];\n\n        let score = 0;"
    
    parts1 = content.split(start_str)
    parts2 = parts1[1].split(end_str)
    
    new_questions = json.dumps(questions, indent=12)
    
    new_content = parts1[0] + "const questions = " + new_questions + end_str + parts2[1]
    
    out_path = os.path.join(week_dir, f'Week_{week_num}_Quiz.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Created {out_path}')

w7_q = [
    {
        "question": "What is the main advantage of 2D (Block) Decomposition over 1D (Slab) Decomposition in large parallel problems?",
        "options": ["It requires less memory per node.", "It minimizes the Surface-to-Volume ratio, thereby reducing communication overhead.", "It is easier to implement using 1D arrays.", "It eliminates the need for synchronization barriers."],
        "correct": 1,
        "explanation": "2D decomposition generally scales better because a block has a smaller perimeter-to-area (surface-to-volume) ratio, minimizing the amount of boundary data that must be communicated between processors."
    },
    {
        "question": "Which parallel motif is characterized by a central node dynamically distributing tasks to a pool of available nodes?",
        "options": ["Fork-Join", "Halo Exchange", "Manager-Worker (Task Farm)", "Divide and Conquer"],
        "correct": 2,
        "explanation": "In the Manager-Worker pattern, a single Manager maintains a pool of work and distributes tasks to Workers, providing excellent dynamic load balancing."
    },
    {
        "question": "In structured grid problems like CFD, what is the purpose of a 'Halo Exchange'?",
        "options": ["To offload computations to a GPU accelerator.", "To exchange boundary ghost cells with neighboring processors before the next compute step.", "To dynamically balance the load among unevenly matched workers.", "To divide a large matrix into smaller sub-matrices."],
        "correct": 1,
        "explanation": "Halo Exchange is used to synchronize boundary data (halos or ghost cells) between adjacent processors in grid-based simulations so they can compute their local updates."
    }
]

create_quiz(7, 'Week 7 - Parallel Algorithms', 'Parallel Algorithms', w7_q)
