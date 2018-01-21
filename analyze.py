import matplotlib.pyplot as plt

from models import load_session, VideoSession


session = load_session()


EMOTIONS = ['anger', 'contempt', 'disgust', 'fear',
            'happy', 'neutral', 'sadness', 'surprise']


def fetchVideoById(video_id):
    return session.query(VideoSession).filter(VideoSession.video_id == video_id).all()


def fetchVideoByName(name):
    return session.query(VideoSession).filter(VideoSession.video.name == name).all()


def get_index(lst, idx):
    try:
        if lst[idx]:
            return True
        return False
    except IndexError:
        return False


def makeAverage(video_sessions):
    average = []
    avg_count = {}
    for i, video_session in enumerate(video_sessions):
        for x, emotions in enumerate(video_session.result):
            if not emotions:
                if not get_index(average, x):
                    average.append([0.0 for x in range(8)])
                avg_count.setdefault(x, 0)
                continue

            if (any(emotions)):
                if x not in avg_count:
                    avg_count[x] = 0
                avg_count[x] += 1

            if not get_index(average, x):
                average.append(emotions)
            else:
                for idx, emotion in enumerate(emotions):
                    average[x][idx] += emotion

    for i, frame in enumerate(average):
        average[i] = [x / avg_count[i] for x in frame]
    return average


def drawGraph(data, expected_moments, amount=0, video='Unknown', fig_num=1):
    plt.figure(fig_num)
    plt.plot(data)

    # set axes ranges
    axes = plt.gca()
    axes.set_ylim([0.0, 1.0])

    # expected emotion lines
    for point in expected_moments:
        plt.axvline(x=point, linestyle='dashed')

    # labels and legends
    plt.xlabel('half seconds of video')
    plt.ylabel('percentage chance for emotion')
    plt.legend(EMOTIONS, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    # titles
    plt.suptitle('Average measured emotions of ' + str(amount) + ' people')
    plt.title('Video: ' + video)

    # plt.show()


def handleVideo(video_id, points):
    video_sessions = fetchVideoById(video_id)
    avg = makeAverage(video_sessions)
    drawGraph(avg, points, amount=len(video_sessions), video=video_sessions[0].video.name, fig_num=video_id)


def main():
    handleVideo(1, points=[19])
    handleVideo(2, points=[])
    handleVideo(3, points=[])
    plt.show()


if __name__ == '__main__':
    main()
