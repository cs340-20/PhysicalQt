# PhysicalQt - Status Report (3/13/2020)
**Team number:** 3
**Team members:**
* Vijay Rajagopal
* Zhenning Yang

#### Introduction
As mentioned in the original proposal, we wanted to create an application that can guide people to do their physical therapy exercises correctly. For this purpose, we used PyQt5 to make a simple UI, which activates the webcam and displays webcam content on the left panel. We also developed a functional pose prediction model that can take an image, then return a skeleton and display it on the right panel. 

For future consideration, we will add functionality to the buttons and add a drop down menu right below the right panel, giving users the flexibility to choose exercises. One issue we are having is that the detection process takes a long time. We plan to use multithreading to elevate some of the performance issues. The main reason behind using multithreading is that Qt5 documentation recommends using a seperate thread for retrieving the webcam stream (secondary thread) and processing the webcam frame onto the GUI (main thread). We also plan on improving the GUI visuals and improve the “evaluation” code.  

#### Customer Value
No changes from initial proposal.

#### Technology
As we described in the proposal, we planned to use QT5 for GUI and user interaction. Qt5 is a C++ powered library and since we want motion detection to happen in real-time, C++ is our first choice. However, we had a lot of trouble trying to set up the proper environment and the ability to quickly prototype and customize UI elements proved are much harder with C++. So, we decided to use PyQt5, which is a python binding of Qt and it is also compatible with Qt designer — an interactive GUI builder (similar to WYSIWYG editors).

In addition to using Qt5 as our GUI platform, we have decided on using a neural network called PoseNet, which can give a 2D estimation of a given pose. The reasoning behind was due to PoseNet’s lower system requirements and output complexity. We are currently using Tensorflow as our neural network platform with PoseNet using MobilenetV1 (101x101) as a feature extractor. MobilenetV1 is a convolutional neural network created by Google and focuses on being able to do classification quickly on mobile and embedded devices, but modifying and using it with Posenet allows Posenet to function with realtime speeds.

Finally, we are also creating an “evaluator” code that can look at a pose, compare it to a given ground truth, and interpret whether an exercise movement has been carried out. As of now, the evaluator is using a single Posenet-processed YouTube video of a person doing jumping jacks. We also added tolerances to each joint in a pose in order to allow a bit more freedom in a user’s movement. The following is a screenshot is a visualization of the evaluator working (red dots - active user movement, white dots - ground truth, green circles - tolerance of user movement):

![alt text](https://i.imgur.com/4zZJbY0.jpg "Visualization demo 1")

![alt text](https://i.imgur.com/jgeJwd9.jpg "Visualization demo 2")

With all of the components combined, we can get a window processing a person’s pose, outputting it (there is a slight bug in scaling and positioning.

![alt text](https://i.imgur.com/J7Q7ckk.jpg "Window demo 1")

In future iterations, we hope to adequately combine them into a highly-efficient, realtime pipeline, which is illustrated below:

![alt text](https://i.imgur.com/MvpZDyb.jpg "diagram of pipeline")

#### Team
Since there are only two of us, Zhenning is focusing on the UI design and Vijay is focusing on the motion detection model. We do not think there will be any future changes to the team roles.

#### Project Management
In terms of whether the product is on track, we believe that we will have to downscale the original concept into something that is still very polished but limited in terms of the number of exercises available. This is because the project ran into two main hindrances that have set us back a couple of weeks. The first one was having to decide what environment we could develop Qt5 in. As discussed in previous sections, the decision ultimately came down to using PyQt5, but there was still a steep learning curve for learning Qt5 libraries and assets. The second hindrance we faced was setting up Posenet in a way to get the highest FPS possible while maintaining a 1080p video input.

Here are the changes to the rest of the schedule:
* **Week 6:** Get first exercise (jumping jacks) working as functional as possible/ Start styling the GUI to look more sleekish/ Improve evaluation
* **Week 7:** Add another exercise/ Improve any performance issues/ Improve evaluation
* **Week 8:** Create a project report and continue debugging the application/ Finishing styling
* **Week 9:** Present project to class

#### Reflection
Overall, the project shows promise on delivering the main objectives outlined in the initial project proposal. The UI development and setup of Posenet took longer than we expected, but with those main hurdles out of the way (for the most part), we can quicken the development of code that can quickly and efficiently detect whether the actual movement is correct. With that being said, the whole process of combining Posenet and Qt5 went fairly quickly mainly due to our familiarity with both increasing. For the next iterations, we want to focus on getting things connected sooner and iron out any bugs that might arise before it's too late.
