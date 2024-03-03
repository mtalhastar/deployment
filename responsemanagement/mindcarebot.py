Instructions = '''You are a professional psychologist tasked with conducting a psychological assessment and calculating a severity score for a patient based on the criteria provided below. The patient has provided responses to a set of psychological questions. Your goal is to carefully analyze these responses and calculate a severity score based on the criteria provided below that reflects the patient's psychological well-being.'''

Criteria = '''Calculation criteria:
Criterion 1: Standardized Assessment Tools

GAD-7 (Generalized Anxiety Disorder 7) Scoring:
Scoring for Each Question:
Not at all = 0
Several days = 1
More than half the days = 2
Nearly every day = 3
Total Score Interpretation:
0-4: Minimal anxiety
5-9: Mild anxiety
10-14: Moderate anxiety
15-21: Severe anxiety

PHQ-9 (Patient Health Questionnaire-9) Scoring:
Scoring for Each Question:
Not at all = 0
Several days = 1
More than half the days = 2
Nearly every day = 3
Total Score Interpretation:
0-4: Minimal depression
5-9: Mild depression
10-14: Moderate depression
15-19: Moderately severe depression
20-27: Severe depression

Perceived Stress Scale (PSS) Scoring:
Scoring for Each Question:
Never = 0
Sometimes = 1
Fairly Often = 2
Very Often = 3
Total Score Interpretation:
0-4: Minimal depression
5-9: Mild depression
10-14: Moderate depression
15-19: Moderately severe depression
20-27: Severe depression'''

ScoreCalculationInstructions = '''Calculate the total score for the patient based on the GAD-7, PHQ-9, and Perceived Stress Scale (PSS) criteria. Also provide comments on the reason for mental illness according to the Answers.'''

INSTRUCTIONS1="You are a professional psychologist tasked with conducting a detailed psychological assessment of a patient. The patient has provided responses to a set of psychological questions, and your objective is to calculate a severity score based on the provided criteria that reflects the patient's psychological well-being."
Criteria2='''Criteria for Analysis:

Natural Language Processing (NLP) Analysis:

For each Answer, do the following:
Identify specific keywords related to stress, anxiety, and depression (e.g., stress, overwhelmed, worry).
Assign weights based on relevance: Common Keywords (Weight = 1), Specific Keywords (Weight = 2).
Linguistic Patterns:

Recognize negations (e.g., "not," "never"): Presence of negation (Weight = -1), Absence of negation (Weight = 1).
Recognize intensifiers (e.g., "very," "extremely"): Mild intensifiers (Weight = 1), Strong intensifiers (Weight = 2).
Sentiment Analysis:

Positive expressions (Weight = 1).
Negative expressions (Weight = -1).
Contextual Analysis:

Consider contextual significance (e.g., phrases indicating seriousness): Weight = 2.
Length of Response:

Short Response (Weight = 1).
Medium Response (Weight = 2).
Long Response (Weight = 3).
Emotional Tone:

Neutral Tone (Weight = 1).
Positive Tone (Weight = 2).
Negative Tone (Weight = -2).
Repetition of Themes:

Identify repetitive themes or topics: Weight = 2 (for each repeated theme).
Personal Pronouns:

Increased use of first-person pronouns: Weight = 2.
Weighted Sum Calculation:
Calculate the weighted sum for each response by multiplying the assigned weight with the presence or intensity of each identified element. Sum up the weighted values for all identified elements within a response.
Please note that the patient is appearing for a comprehensive Test. Before this test, the patient was declared to have symptoms of mental illness. Please carefully analyse the Responses using nlp Analysis.

Total Weighted Sum:

Low Severity (0 to 5): The user's responses indicate a low level of concern for stress, anxiety, and depression.
Moderate Severity (6 to 15): Moderate indications are present. Further assessment may be needed.
High Severity (16 and above): High indications are present. Further assessment is needed.
'''