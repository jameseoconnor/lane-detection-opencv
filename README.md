# camera-parameter-finder
camera parameter finding module for my colllege assignment using OpenCV

# Evaluating Lane Detection Algorithm in Multiple Scenarios Using Hough Transform

James O&#39;Connor

_IT Sligo_

**Abstract**

In this paper the application of an edge detection algorithm was explored using Canny edge detection and the Hough Transform. The Hough Transform algorithm, and its associated hyperparameters was tested in eight distinct road scenarios using a test framework. Results were compared to determine the optimal hyperparameters as well as determining the effect of influential factors on the performance.

# Introduction

Edge detection algorithms have been used for a number of years for various applications . One of the key applications of edge detection algorithms in the autonomous vehicles industry is lane detection. Lane detection is the critical component in the application of various features in intelligent vehicles. Examples of these include lane detection warning (LDW), lane departure prevention (LDP) as well as enabling autonomous and driverless vehicles to perceive their environments and navigate. LWD and LDP systems have been shown to reduce crashes by 26% and 32% respectively (NHTSA, 2016) and have become such a critical component of intelligent vehicles that they will become mandatory in all vehicles within the EU by 2022 (European Parliament, 2019).

In many computer vision problems concerning intelligent vehicles, such as pedestrian and object detection, sensor fusion of cameras with ranging sensors such as LiDAR, RADAR can complement the overall object detection capabilities of the intelligent vehicles. Similarly, they can act as a redundancy in the event of low visibility conditions or a compromised camera sensor. However, lane detection algorithms rely solely on the input from the camera (or cameras) to perform a classification. Adverse weather conditions affect the cameras range of visibility (snow, rain, fog), the ability to find occluded road markings (snow) or contrast (sunny). Therefore, developing a robust, high availability lane detectors using camera input is critical to the safety and reliability of these systems. Code for this paper can be found [here](https://github.com/jameseoconnor/lane-detection-opencv).


# Review of Literature

## Algorithm Design

The original edge finding algorithm was proposed by John Canny (Canny, 1986) uses the first derivative of the change between pixels in all four directions to calculate the gradient and direction of an edge. The Hough Transform (US Patent No. US3069654A, 1960) can be used on top of this to distinguish the presence of lines within these edges, based on a number of hyperparameters.

## Testing

There does not seem to be a consensus on how to test lane following algorithms, however there is a number of datasets that are used as benchmarks. One of these is the KITTI dataset which includes 289 training and 290 test images that have been labelled and can be used to benchmark lane detection algorithms. Bush &amp; Esposito (2010) adopted a simple testing approach to evaluation the performance by manually assigning the classification a score from 0 to 3, 3 being excellent and 0 being detrimental. Nguyen, Pham, Kim, &amp; Jeon (2008) defined a test framework for the accuracy of line detection by Hough Transform and involves counting the number of lines predicted and comparing to the true value and calculates the false positives and negatives.


# Method

## Algorithm Design

The algorithm design was based on Yoo, Lee, Park, &amp; Kim (2017) and code by pknowledge (2020) and is outlined in Figure 1. This algorithm was be repeated for each frame of the video The sample videos ran at 24 FPS and resolution 720p on a 2 GHz Quad-Core Intel Core i5.

![Shape2](RackMultipart20211203-4-1n4bcgn_html_df0168c6e56d40ca.gif)

**Figure 1: Algorithm Design**

**Scenario Generation**

As the goal of this paper is to investigate the efficacy of a lane detection algorithm in different scenarios, the initial step was to design the test scenarios based on the video selected for analysis. Xia, Duan, Gao, Hu, &amp; He (2018) provide a test scenario design framework for intelligent vehicles that ensures adequate coverage and effectiveness. The framework works as follows: decide the influential factors, rank them by degree of importance, create combinatorial test cases for all of these factors and then group them into larger test cases. The figures below were taken from the paper, which lists a number of influential factors including environment, road, traffic and vehicle dynamics. However, for the sake of brevity, as well as not having access to vehicle dynamics data, the factors were not weighted and only environment camera and traffic conditions were considered as test case variables.


![Figure_2](static/Figure_2.jpg)


From these influential factors, eight scenarios were derived as seen in Table 1. These test scenarios were designed to give a high coverage of each influential factor.

**Table 1: Test Scenarios**

|
 | **Environmental Factors** | **Camera** | **Traffic** |
| --- | --- | --- | --- |
| **Scenario #** | **Weather** | **Time** | **Light Change** | **Angle** | **Vehicle Flow** |
| 1 | Fine (B) | Daytime | No Change | Low | 10 |
| 2 | Fine (B) | Daytime | None | Normal | 10 |
| 3 | Fine (B) | Daytime | Tunnel | Normal | 80 |
| 4 | Fine (B) | Night Streetlight | None | Low | 10 |
| 5 | Fine (O) | Night No Streetlight | None | Normal | 80 |
| 6 | Fine (O) | Daytime | No Change | High | 80 |
| 7 | Rain (H) | Daytime | No Change | High | 10 |
| 8 | Rain (L) | Daytime | None | Normal | 10 |

## Algorithm Testing

The algorithm was tested under **two conditions** :

1. Altering the hyper parameters over multiple runs of the same video to determine the effects of hyperparameters on the same scenario.
2. Altering the scenario over multiple runs to test the robustness of the algorithm.

To test the first condition (i), the following hyper parameters permutations for the Probabilistic Hough Line were used.

**Table 2: Variations of Hyperparameters**

| **Run #** | **rho** | **theta** | **threshold** | **min\_line\_length** | **max\_line\_gap** |
| --- | --- | --- | --- | --- | --- |
| Run 1 | 1 | pi/180 | 90 | 50 | 90 |
| Run 2 | 2 | pi/180 | 90 | 50 | 90 |
| Run 3 | 1 | pi/180 | 50 | 50 | 100 |
| Run 4 | 1 | pi/180 | 80 | 25 | 50 |
| Run 5 | 2 | pi/90 | 80 | 10 | 150 |

The outcome of the optimal hyperparameter permutation from condition (i) was used to test the second condition (ii). As this research is being conducted on an unlabelled dataset, the KITTI dataset could not be used to benchmark performnce without extensive image labelling. The approach by Nguyen, Pham, Kim, &amp; Jeon (2008) was used to measure the correctness of the algorithm. This framework involves counting the number of lines predicted in a frame and comparing to the true value (N = Number of Lines). Equations for each column are outlined in the original paper. Sample frames were taken at 20, 40, 60, 80 and 100 frames so they could be analysed to evaluate the performance of the algorithm in both condition (i) and condition (ii).

1.
# Results &amp; Discussion

Images can be found [here](https://github.com/jameseoconnor/lane-detection-opencv/tree/main/output) of each frame from each run and scenario tested.

## Condition (i) - Effect Of Hyper Parameters

A total of five runs were completed using the Hough Lines hyper parameters outlined in Table 3.

**Table 3: Run 1 Sample Frame Analysis**

| **Sample Frame** | **N\_True** | **N\_Detected** | **N\_Correct** | **N\_Duplicate** | **N\_Superfluous** | **N\_False\_Negatives** | **N\_False\_Positives** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 2 | 3 | 1 | 2 | 0 | 1 | 0.6667 |
| 40 | 2 | 5 | 2 | 3 | 0 | 0 | 0.6000 |
| 60 | 2 | 3 | 1 | 2 | 0 | 1 | 0.6667 |
| 80 | 2 | 4 | 2 | 2 | 0 | 0 | 0.5000 |
| 100 | 1 | 2 | 1 | 1 | 0 | 0 | 0.5000 |
| **Total** | **9** | **17** | **7** | **10** | **0** | **2** | **2.93** |

![](RackMultipart20211203-4-1n4bcgn_html_750d2f4af24c41f.jpg) ![](RackMultipart20211203-4-1n4bcgn_html_b5d7508652b6124c.jpg)

**Figure 3: Run 1 - Frame 20 - 2 Lines Visible - 3 Lines Detected – 1 Correct – 2 Duplicate**

**Table 4: Overall Results**

| **Run #** | **N\_True** | **N\_Detected** | **N\_Correct** | **N\_Duplicate** | **N\_Superfluous** | **N\_False\_Negatives** | **N\_False\_Positives** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | 17 | 7 | 10 | 0 | 2 | 2.93 |
| 2 | 9 | 19 | 7 | 12 | 0 | 2 | 2.43 |
| 3 | 9 | 20 | 7 | 13 | 0 | 2 | 3.18 |
| 4 | 8 | 18 | 7 | 11 | 0 | 0 | 3.03 |
| 5 | 8 | 21 | 7 | 14 | 0 | 0 | 3.23 |

Each run identified the same number of correct line predictions. Run 1 performed the best as it had the lowest duplicate line rate and lowest false positive rate. Lowering the threshold increased the false positive rate as seen in Run 3. Increasing rho and lowering theta also increased the false positive rate as seen in Run 5.

## Condition (i) - Effect Of Scenarios

Using the parameters from condition (i), the same approach was taken to test the in the eight scenarios outlined in Table 6.

**Table 5: Scenario 1 Sample Frame Analysis**

| **Sample Frame** | **N\_True** | **N\_Detected** | **N\_Correct** | **N\_Duplicate** | **N\_Superfluous** | **N\_False\_Negatives** | **N\_False\_Positives** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 2 | 5 | 2 | 2 | 1 | 0 | 0.6 |
| 40 | 2 | 3 | 1 | 2 | 0 | 1 | 0.667 |
| 60 | 2 | 2 | 1 | 1 | 0 | 1 | 0.5 |
| 80 | 2 | 2 | 1 | 1 | 0 | 1 | 0.5 |
| 100 | 1 | 5 | 1 | 2 | 2 | 0 | 0.8 |
| Total | 9 | 17 | 6 | 8 | 3 | 3 | 3.067 |

**Table 6: Overall Results**

| **Scenario#** | **N\_True** | **N\_Detected** | **N\_Correct** | **N\_Correct %** | **N\_Duplicate** | **N\_Superfluous** | **N\_False\_Negatives** | **N\_False\_Positives** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | 17 | 6 | 66.67% | 8 | 3 | 3 | 3.07 |
| 2 | 12 | 13 | 5 | 41.67% | 6 | 2 | 7 | 2.33 |
| 3 | 11 | 16 | 11 | 100.00% | 5 | 0 | 0 | 1.05 |
| 4 | 10 | 17 | 8 | 80.00% | 9 | 0 | 2 | 1.82 |
| 5 | 9 | 13 | 8 | 88.89% | 5 | 0 | 1 | 1.73 |
| 6 | 9 | 17 | 8 | 88.89% | 9 | 0 | 1 | 2.07 |
| 7 | 4 | 0 | 0 | 0.00% | 0 | 0 | 4 | 0.00 |
| 8 | 10 | 20 | 10 | 100.00% | 10 | 0 | 0 | 0.00 |

Scenario 3 and scenario 8 scored the highest overall. Interestingly, scenario 8 included light rain but scored the same as a bright day. Clear road markings had a very positive impact on detection. Heavy rain had a very negative impact as seen in scenario 7. Normal to High angled camera angles scored better than low angled shots due to more of the line being available to classify. Scenario 2 had a number of bends and direct sunlight exposure which resulted in a low classification score.

1.
# Conclusion and Future Research

To conclude, the research showed that the scenario and the Hough Transform hyperparameters both affect the performance of the algorithm, but the former to a much larger extent. Ultimately there are a multitude of variables to contend with, making generalizing a model that works in all situations very difficult. There are a number of directions this research can take. In terms of test case generation, a wider set of test cases can be undertaken to include other environmental factors such as vehicle dynamics, road marking definition and traffic. Different colour scales such as HSV (hue, saturation, value) or HLS (hue, lightness, saturation) could be tested during image pre-processing phase of the algorithm to better expose the road markings. Logic to determine the vanishing point could be added to the algorithm to dynamically set create a dynamic mask to optimise the computation area of the images on which we run Canny detection and Hough Transform. Similarly, experiments could be conducted to determine the optimal parameters for each scenario and a scenario detection algorithm using a Convolutional Neural Network (CNN) could be used to detect the scenario type and set the parameters accordingly.

# Bibliography

Bush, F. N., &amp; Esposito, J. M. (2010). Vision-based lane detection for an autonomous ground vehicle: A comparative field test. _Southeastern Symposium on System Theory (SSST)_.

Canny, J. (1986). A Computational Approach to Edge Detection . _IEEE Transactions on Pattern Analysis and Machine Intelligence_.

European Parliament. (2019, 02 20). _www.europarl.europa.eu._ Retrieved 03 10, 2021, from https://www.europarl.europa.eu/news/en/press-room/20190220IPR27656/safer-roads-more-life-saving-technology-to-be-mandatory-in-vehicles

Hough, P. (1960). _US Patent No. US3069654A._

Nguyen, T. T., Pham, X. D., Kim, D., &amp; Jeon, J. W. (2008). A test framework for the accuracy of line detection by Hough Transforms. _2008 6th IEEE International Conference on Industrial Informatics._ Daejeon: IEEE.

NHTSA. (2016). _POTENTIAL SAFETY BENEFITS OF LANE DEPARTURE WARNING AND PREVENTION SYSTEMS IN THE U.S. VEHICLE FLEET ._ Retrieved 03 12, 2021, from https://www-esv.nhtsa.dot.gov/Proceedings/24/files/24ESV-000080.PDF

pknowledge. (2020). _Road Lane Line Detection with OpenCV_. Retrieved from GitHub: https://gist.github.com/pknowledge/86a148c6cd5f0f2820ba81561cc00a8e

Xia, Q., Duan, J., Gao, F., Hu, Q., &amp; He, Y. (2018). Test Scenario Design for Intelligent Driving System Ensuring Coverage and Effectiveness. _International Journal of Automotive Technology volume_.

Yoo, J. H., Lee, S.-W., Park, S.-K., &amp; Kim, D. H. (2017). A Robust Lane Detection Method Based on Vanishing Point Estimation Using the Relevance of Line Segments. _IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS_.