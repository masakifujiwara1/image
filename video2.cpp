#include <opencv2/opencv.hpp>
#include <iostream>

using namespace std;
using namespace cv;

int main() {
    VideoCapture cap('hand_video.mp4');
    Mat frame;

    while (1) {
        cap >> frame;

        Mat hsv;
        cvtColor(frame, hsv, COLOR_BGR2HSV);
        Mat hue;
        extractChannel(hsv, hue, 0);

        inRange(hue, 2, 10, hue);

        medianBlur(hue, hue, 9);

        Mat output;
        copyTo(frame, output, hue);

        imshow("output", output);

        int key = waitKey(1);
        if (key == 27) { //escが押されたら終了
            break;
        }
    }

    return 0;
}
