#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace std;
using namespace cv;

const int slider_max = 100;
int low_slider,high_slider;
int high = 30,low = 1;
char TrackbarName[50];

Mat frame0gray,frame1gray;
Mat dispbm,dispsgbm;
Mat dispnorm_bm,dispnorm_sgbm;
Mat falseColorsMap, sfalseColorsMap;
Mat frame0,frame1;
Mat grayLeft,grayRight;
Vec3i d,c;
static void on_trackbar( int, void* )
{
   low =  low_slider;
   high = high_slider;

   vector<Vec3f> circlesL;
   HoughCircles(grayLeft, circlesL, HOUGH_GRADIENT, 1,
                 grayLeft.rows/16, // change this value to detect circles with different distances to each other
                 100, 30, low, high // change the last two parameters
                                // (min_radius & max_radius) to detect larger circles
                 );
   vector<Vec3f> circlesR;
   HoughCircles(grayRight, circlesR, HOUGH_GRADIENT, 1,
                 grayRight.rows/16, // change this value to detect circles with different distances to each other
                 100, 30, low, high // change the last two parameters
                                // (min_radius & max_radius) to detect larger circles
                 );

   for( size_t i = 0; i < circlesL.size(); i++ )
   {
      c = circlesL[i];
      circle( frame0, Point(c[0], c[1]), c[2], Scalar(0,0,255), 3, LINE_AA);
      circle( frame0, Point(c[0], c[1]), 2, Scalar(0,255,0), 3, LINE_AA);
   }
   for( size_t i = 0; i < circlesR.size(); i++ )
   {
      d = circlesR[i];
      circle( frame1, Point(d[0], d[1]), d[2], Scalar(0,0,255), 3, LINE_AA);
      circle( frame1, Point(d[0], d[1]), 2, Scalar(0,255,0), 3, LINE_AA);
   }

   fprintf(stderr,"l[%d] h[%d] x_posL[%i] \n",low,high,c[0]);
   fprintf(stderr,"l[%d] h[%d] x_posR[%i] \n",low,high,d[0]);
      imshow("detected circles Left", frame0);
      imshow("detected circles Right", frame1);
}

int main()
{   
   
   int ndisparities = 16*5;   /**< Range of disparity */
   int SADWindowSize = 21; /**< Size of the block window. Must be odd */
   Ptr<StereoBM> sbm = StereoBM::create( ndisparities, SADWindowSize );
   Ptr<StereoSGBM> sgbm = StereoSGBM::create(0,    //int minDisparity
                                    96,     //int numDisparities
                                    5,      //int SADWindowSize
                                    600,    //int P1 = 0
                                    2400,   //int P2 = 0
                                    10,     //int disp12MaxDiff = 0
                                    16,     //int preFilterCap = 0
                                    2,      //int uniquenessRatio = 0
                                    20,    //int speckleWindowSize = 0
                                    30,     //int speckleRange = 0
                                    true);  //bool fullDP = false
   //-- Check its extreme values
   double minVal; double maxVal;
   // while(true) 
   // {
      //grab and retrieve each frames of the video sequentially 
      // camera0 >> 
      frame0 = imread("frameL_20.jpg",1);
      // camera1 >> 
      frame1 = imread("frameR_20.jpg",1);

      imshow("Video0", frame0);
      imshow("Video1", frame1);
      cvtColor(frame0,frame0gray,CV_BGR2GRAY);
      cvtColor(frame1,frame1gray,CV_BGR2GRAY);

      sbm->compute( frame0gray, frame1gray, dispbm );
      minMaxLoc( dispbm, &minVal, &maxVal );
      dispbm.convertTo( dispnorm_bm, CV_8UC1, 255/(maxVal - minVal));

      sgbm->compute(frame0gray, frame1gray, dispsgbm);
      minMaxLoc( dispsgbm, &minVal, &maxVal );
      dispsgbm.convertTo( dispnorm_sgbm, CV_8UC1, 255/(maxVal - minVal));

      imshow( "BM", dispnorm_bm);
      imshow( "SGBM",dispnorm_sgbm);

      grayLeft = frame0gray;
      grayRight = frame1gray;
      
      low_slider = 0;
      high_slider = 0;
      
      medianBlur(grayLeft, grayLeft, 5);
      medianBlur(grayRight, grayRight, 5);

       // Create Window
      namedWindow("myThreshold", WINDOW_NORMAL);
      createTrackbar( "LowThreshold", "myThreshold", &low_slider, slider_max, on_trackbar );
      // on_trackbar( low_slider,0 );
      createTrackbar( "HighTreshold", "myThreshold", &high_slider, slider_max, on_trackbar );
      // on_trackbar( high_slider,0 );
      

         //wait for 40 milliseconds
      // sprintf( TrackbarName, "Alpha x %d", slider_max );
      cvWaitKey();
//          if(27 == char(c)) break;
//  return 0;
}
