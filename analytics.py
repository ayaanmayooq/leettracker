import matplotlib.pyplot as plt

def plot_topic_strength(data):
    topics = {}
    for problem in data['stat_status_pairs']:
        for topic in problem.get('topics', []):
            topics[topic] = topics.get(topic, 0) + 1

    topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
    plt.bar(topics.keys(), topics.values())
    plt.xlabel('Topics')
    plt.ylabel('Number of Problems')
    plt.title('Topic Strength')
    plt.xticks(rotation=45)
    plt.show()
