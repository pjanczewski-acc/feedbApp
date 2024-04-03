import unittest
from datetime import datetime, timedelta

def filter_feedback(feedback_table, months_back):
    delta = timedelta(days=months_back * 30)
    threshold_date = datetime.now() - delta
    filtered_feedback = [entry for entry in feedback_table if entry['Date'] >= threshold_date]
    return filtered_feedback

def generate_feedback_scenario(filtered_feedback):
    positive_achievements = []
    areas_of_improvement = []
    key_strengths = []

    for entry in filtered_feedback:
        feedback = entry['Feedback']
        if 'positive' in feedback.lower() or 'great' in feedback.lower() or 'excellent' in feedback.lower():
            positive_achievements.append(feedback)
        elif 'improvement' in feedback.lower() or 'needs' in feedback.lower() or 'should work on' in feedback.lower():
            areas_of_improvement.append(feedback)
        else:
            key_strengths.append(feedback)

    scenario = []

    if positive_achievements:
        scenario.append("Specific Positive Achievements:")
        for achievement in positive_achievements:
            scenario.append(f"- {achievement}")

    if areas_of_improvement:
        scenario.append("\nAreas of Improvement:")
        for improvement in areas_of_improvement:
            scenario.append(f"- {improvement}")

    if key_strengths:
        scenario.append("\nOverall Key Strengths to Build on in the Future:")
        for strength in key_strengths:
            scenario.append(f"- {strength}")

    return scenario

class TestFeedbackFunctions(unittest.TestCase):
    def test_filter_feedback(self):
        feedback_table = [
            {'Date': datetime.strptime('15.10.2023', '%d.%m.%Y')},
            {'Date': datetime.strptime('20.11.2023', '%d.%m.%Y')},
            {'Date': datetime.strptime('05.01.2024', '%d.%m.%Y')}
        ]
        months_back = 3
        filtered_feedback = filter_feedback(feedback_table, months_back)
        self.assertEqual(len(filtered_feedback), 2)

    def test_generate_feedback_scenario(self):
        filtered_feedback = [
            {'Feedback': 'Made significant progress in completing project tasks on time.'},
            {'Feedback': 'Needs improvement in communication with team members.'},
            {'Feedback': 'Demonstrates excellent teamwork skills and collaboration abilities.'}
        ]
        scenario = generate_feedback_scenario(filtered_feedback)
        self.assertEqual(len(scenario), 3)

if __name__ == '__main__':
    unittest.main()
