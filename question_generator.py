# question_generator.py
# -------------------------------------------------------
# Generates role-specific and skill-specific interview
# questions based on predicted job role and detected skills.
# -------------------------------------------------------

import random

# ---------------------------------------------------------------------------
# Master question bank: keyed by skill (lowercase) and by job role
# ---------------------------------------------------------------------------

SKILL_QUESTIONS = {
    "python": [
        "Explain the difference between a list and a tuple in Python.",
        "What are Python decorators and how do you use them?",
        "How does Python's garbage collection work?",
        "What is the Global Interpreter Lock (GIL) in Python?",
        "Explain list comprehensions and when you would use them.",
        "What are generators in Python and how do they differ from iterators?",
        "How do you handle exceptions in Python? Give an example.",
        "What is the difference between deep copy and shallow copy?",
        "Explain the concept of *args and **kwargs.",
        "What are Python's magic (dunder) methods? Give examples.",
    ],
    "machine learning": [
        "What is overfitting and how do you prevent it?",
        "Explain the bias-variance tradeoff.",
        "What is cross-validation and why is it important?",
        "Describe the difference between supervised and unsupervised learning.",
        "What is gradient descent and how does it work?",
        "Explain precision, recall, and F1-score.",
        "What is regularization? Explain L1 and L2 regularization.",
        "How does a Random Forest work?",
        "What is feature engineering and why does it matter?",
        "Explain the ROC curve and AUC.",
    ],
    "deep learning": [
        "What is backpropagation and how does it work?",
        "Explain the vanishing gradient problem and solutions.",
        "What are CNNs and what are they used for?",
        "What is dropout and why is it used?",
        "Explain batch normalization.",
        "What is transfer learning?",
        "Describe the architecture of a Transformer model.",
        "What is an LSTM and how does it handle sequential data?",
        "What is attention mechanism in neural networks?",
        "Explain the difference between RNN, LSTM, and GRU.",
    ],
    "sql": [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "Explain the difference between WHERE and HAVING.",
        "What are window functions in SQL? Give an example.",
        "What is database normalization? Explain 1NF, 2NF, 3NF.",
        "What is an index and how does it improve query performance?",
        "Explain ACID properties in databases.",
        "What is the difference between DELETE, TRUNCATE, and DROP?",
        "What are CTEs (Common Table Expressions)?",
        "How would you optimize a slow SQL query?",
        "What is a stored procedure and when would you use one?",
    ],
    "javascript": [
        "What is the difference between var, let, and const?",
        "Explain closures in JavaScript.",
        "What is the event loop in JavaScript?",
        "What are Promises and async/await?",
        "Explain prototypal inheritance in JavaScript.",
        "What is the difference between == and ===?",
        "What are arrow functions and how do they differ from regular functions?",
        "Explain the concept of hoisting.",
        "What is the DOM and how do you manipulate it?",
        "What are higher-order functions? Give examples.",
    ],
    "react": [
        "What is the Virtual DOM and how does React use it?",
        "Explain the difference between state and props.",
        "What are React hooks? Explain useState and useEffect.",
        "What is the Context API and when would you use it?",
        "Explain the React component lifecycle.",
        "What is Redux and when should you use it?",
        "How does React handle forms?",
        "What is reconciliation in React?",
        "Explain React.memo and useMemo.",
        "What are controlled vs uncontrolled components?",
    ],
    "java": [
        "What is the difference between JDK, JRE, and JVM?",
        "Explain OOP concepts: encapsulation, inheritance, polymorphism, abstraction.",
        "What is the difference between an interface and an abstract class?",
        "How does garbage collection work in Java?",
        "What are Java Streams and how do you use them?",
        "Explain the difference between HashMap and Hashtable.",
        "What is multithreading? How do you create a thread?",
        "What are checked vs unchecked exceptions?",
        "Explain the SOLID principles.",
        "What is dependency injection?",
    ],
    "docker": [
        "What is Docker and how does it differ from a virtual machine?",
        "Explain the difference between a Docker image and a container.",
        "What is a Dockerfile and what are common instructions?",
        "How do Docker volumes work?",
        "Explain Docker networking.",
        "What is Docker Compose and when do you use it?",
        "How do you optimize Docker image size?",
        "What is a multi-stage build in Docker?",
        "How do you manage secrets in Docker?",
        "What is Docker Swarm?",
    ],
    "kubernetes": [
        "What is Kubernetes and what problem does it solve?",
        "Explain the difference between a Pod, Deployment, and Service.",
        "What is a ConfigMap and a Secret in Kubernetes?",
        "How does Kubernetes handle auto-scaling?",
        "What is a Kubernetes Ingress?",
        "Explain rolling updates and rollbacks in Kubernetes.",
        "What are namespaces in Kubernetes?",
        "How does Kubernetes service discovery work?",
        "What is Helm and why is it useful?",
        "Explain the concept of a DaemonSet.",
    ],
    "aws": [
        "What are the key AWS services you have worked with?",
        "Explain the difference between EC2 and Lambda.",
        "What is S3 and what are its storage classes?",
        "How does AWS IAM work?",
        "What is Auto Scaling and Elastic Load Balancing?",
        "Explain VPC and subnets in AWS.",
        "What is CloudFormation?",
        "Explain the difference between RDS and DynamoDB.",
        "What is AWS CloudWatch used for?",
        "How would you architect a highly available application on AWS?",
    ],
    "nlp": [
        "What is tokenization in NLP?",
        "Explain TF-IDF and its applications.",
        "What is word embedding? Explain Word2Vec.",
        "What is Named Entity Recognition (NER)?",
        "Explain the Transformer architecture used in BERT and GPT.",
        "What is sentiment analysis and how do you implement it?",
        "What are stop words and why are they removed?",
        "Explain stemming vs lemmatization.",
        "What is a language model?",
        "How does attention mechanism improve NLP tasks?",
    ],
    "tensorflow": [
        "What is a tensor and how is it used in TensorFlow?",
        "Explain the difference between TensorFlow 1.x and 2.x.",
        "How do you build and train a neural network in TensorFlow/Keras?",
        "What is eager execution in TensorFlow?",
        "Explain the concept of a computation graph.",
        "How do you save and load models in TensorFlow?",
        "What are callbacks in Keras?",
        "Explain data pipelines using tf.data.",
        "What is TensorBoard and how do you use it?",
        "How do you deploy a TensorFlow model?",
    ],
    "pytorch": [
        "What is the difference between PyTorch and TensorFlow?",
        "Explain dynamic vs static computation graphs.",
        "How does autograd work in PyTorch?",
        "What is a DataLoader in PyTorch?",
        "How do you define a custom neural network in PyTorch?",
        "Explain the training loop in PyTorch.",
        "What is torch.no_grad() used for?",
        "How do you handle GPU acceleration in PyTorch?",
        "What are PyTorch Lightning and its benefits?",
        "How do you serialize a PyTorch model?",
    ],
    "rest api": [
        "What is REST and what are its constraints?",
        "What is the difference between PUT and PATCH?",
        "How do you handle authentication in a REST API?",
        "What are HTTP status codes? Give examples.",
        "What is CORS and how do you handle it?",
        "Explain statelessness in REST APIs.",
        "What is API versioning and why is it important?",
        "How do you design a RESTful endpoint structure?",
        "What is OpenAPI/Swagger?",
        "How would you handle rate limiting in an API?",
    ],
    "data analysis": [
        "What is exploratory data analysis (EDA)?",
        "How do you handle missing data?",
        "Explain the difference between correlation and causation.",
        "What is an outlier and how do you detect/handle it?",
        "What statistical tests do you use for hypothesis testing?",
        "How do you handle imbalanced datasets?",
        "What is feature scaling and when is it necessary?",
        "Explain dimensionality reduction techniques.",
        "What is A/B testing?",
        "How do you communicate data insights to non-technical stakeholders?",
    ],
}

# Role-specific behavioral/conceptual questions
ROLE_QUESTIONS = {
    "Data Scientist": [
        "Walk me through your typical data science project workflow.",
        "How do you approach a new dataset you've never seen before?",
        "How do you communicate complex model results to business stakeholders?",
        "Describe a time when your model performed poorly in production. What did you do?",
        "What metrics would you use to evaluate a recommendation system?",
        "How do you decide which machine learning algorithm to use for a problem?",
        "What is your approach to feature selection?",
        "How do you ensure your model doesn't have bias?",
    ],
    "Backend Developer": [
        "How do you design a scalable backend system?",
        "What is caching and how would you implement it?",
        "Explain the CAP theorem.",
        "How do you handle database migrations in production?",
        "What design patterns do you commonly use?",
        "How do you approach API security?",
        "Describe your approach to logging and monitoring.",
        "How do you handle asynchronous tasks in a backend system?",
    ],
    "Frontend Developer": [
        "How do you optimize website performance?",
        "What are Core Web Vitals and why do they matter?",
        "Explain responsive design and how you implement it.",
        "How do you ensure cross-browser compatibility?",
        "What is your approach to accessibility (a11y)?",
        "How do you manage state in large frontend applications?",
        "What is lazy loading and when do you use it?",
        "How do you approach CSS architecture for large projects?",
    ],
    "ML Engineer": [
        "What is MLOps and why is it important?",
        "How do you monitor a machine learning model in production?",
        "Explain model drift and how to detect it.",
        "How do you design an end-to-end ML pipeline?",
        "What tools do you use for experiment tracking?",
        "How do you handle model versioning?",
        "Describe your approach to model serving at scale.",
        "How do you ensure reproducibility in ML experiments?",
    ],
    "DevOps Engineer": [
        "What is the difference between CI and CD?",
        "How do you design a zero-downtime deployment?",
        "What is infrastructure as code? Which tools have you used?",
        "How do you handle incident response?",
        "Explain blue-green deployments vs canary releases.",
        "What is your approach to secrets management?",
        "How do you monitor system health?",
        "Describe your experience with container orchestration.",
    ],
    "Full Stack Developer": [
        "How do you decide what logic belongs on the frontend vs backend?",
        "Describe your approach to API design.",
        "How do you handle user authentication and authorization?",
        "What is your strategy for database design?",
        "How do you ensure security in a full stack application?",
        "Describe your CI/CD workflow.",
        "How do you approach performance optimization across the stack?",
        "What is your experience with cloud deployment?",
    ],
    "Android Developer": [
        "Explain the Android Activity lifecycle.",
        "What is the difference between a Service and an IntentService?",
        "How do you handle background tasks in Android?",
        "What are Android Jetpack components?",
        "How do you optimize an Android app for performance?",
        "Explain MVVM architecture in Android.",
        "How do you handle different screen sizes?",
        "What is ProGuard and why is it used?",
    ],
    "Database Administrator": [
        "How do you approach query optimization?",
        "Explain your backup and disaster recovery strategy.",
        "How do you handle database replication?",
        "What is database sharding?",
        "How do you monitor database performance?",
        "Explain locking and deadlocks in databases.",
        "What is your approach to capacity planning?",
        "How do you handle schema migrations in production?",
    ],
    "QA Engineer": [
        "What is the difference between functional and non-functional testing?",
        "Explain test-driven development (TDD).",
        "How do you decide what to automate vs test manually?",
        "What is your approach to writing a test plan?",
        "How do you test APIs?",
        "What is regression testing?",
        "Describe your experience with CI/CD pipelines for testing.",
        "How do you prioritize bug fixing?",
    ],
}

# General interview questions applicable to any role
GENERAL_QUESTIONS = [
    "Tell me about yourself and your technical background.",
    "What is your greatest technical strength?",
    "Describe a challenging project you worked on and how you overcame obstacles.",
    "How do you keep up with the latest trends in technology?",
    "How do you handle tight deadlines and competing priorities?",
    "Describe your experience working in an Agile environment.",
    "Where do you see yourself in 5 years?",
    "Why are you interested in this role?",
    "Describe your ideal work environment.",
    "What's a recent technical concept you learned? How did you apply it?",
]


def generate_questions(skills: list, job_role: str, num_questions: int = 8) -> dict:
    """
    Generate categorized interview questions based on detected skills and job role.

    Args:
        skills      : List of skill strings extracted from the resume.
        job_role    : Predicted job role string.
        num_questions: Total target question count.

    Returns:
        A dict with keys 'skill_based', 'role_based', 'general'.
    """
    skill_based = []
    used_skills = set()

    # Collect skill-specific questions (shuffle for variety)
    for skill in skills:
        skill_lower = skill.lower()
        for key, questions in SKILL_QUESTIONS.items():
            if key in skill_lower or skill_lower in key:
                if key not in used_skills:
                    # Pick 2 random questions per matched skill
                    selected = random.sample(questions, min(2, len(questions)))
                    skill_based.extend(selected)
                    used_skills.add(key)
                break  # avoid double-matching

    # Deduplicate and cap at num_questions
    skill_based = list(dict.fromkeys(skill_based))[:num_questions]

    # Role-specific questions
    role_based = ROLE_QUESTIONS.get(job_role, [])
    role_based = random.sample(role_based, min(3, len(role_based)))

    # General questions
    general = random.sample(GENERAL_QUESTIONS, 3)

    return {
        "skill_based": skill_based,
        "role_based": role_based,
        "general": general,
    }
