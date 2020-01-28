## PhysicalQt
------
### Team name: doktors
### Created by: Vijay Rajagopal, Zhenning Yang
------
### Purpose
Regardless of what type of childhood a person has had, it is most likely that they have been physically injured in some way or another. Depending on the severity of the injury, the usage of physical therapy, which are a various assortment of exercises, stretches, and movements, can restore a person’s motor skills quite significantly, but this requires the person doing these activities to do them correctly. This is where our idea of creating a program that can help a person do an exercise appropriately comes from. A program which can quickly and accurately track a person’s movement and the type of physical exercise their supposed to do can immensely help with their recovery. This type of program has not been really implemented in a way where tracking is not hindered by sensors or other cumbersome methods.

### Customer Needs
Our main customer would be an out-patient that has been assigned various physical therapy exercises by their physical therapist or doctor. These patients could likely have never done such an exercise, and when they are left to their own devices to do that exercise they could execute it incorrectly and could hinder their recovery phase.

#### Solution
PhysicalQt can provide a patient the ability to know that they are doing their physical therapy exercises correctly. This is incredibly valuable for the customer and their recovery process as well as gives peace of mind for other parties such as their doctors as well as friends and family. 

#### Success Markers
PhysicalQt's marker of success would be its ability to accurately judge a person's exercise as well as how easy it is to pick up and use for the customer.

### Technology
PhysicalQt will be mainly relying on Qt5, a C++ powered library, for the GUI and user interaction. The ability to detect if a person’s exercise movement will require a pose estimation model that is able to take in an image frame from a camera, compute the general pose of the figure, and output coordinates in 2D space. All of this has to happen in real time to provide the best user experience. A couple of models could have the ability to this; some of these models include [PoseNet](https://www.tensorflow.org/lite/models/pose_estimation/overview), a 2015 neural network able to run with low inference speed and average accuracy, and [OpenPose](https://github.com/tensorlayer/openpose-plus), a similar neural network that can achieve higher accuracy but with a lower inference speed versus PoseNet. Both of these networks are written in Python with a library called Tensorflow, but due to the conflicting performance of Python and C++ programs, these models can be called with a Tensorflow C++ API for a performance boost.

![image showing a lady moving around and a blue skeleton moving with her](https://www.tensorflow.org/images/lite/models/pose_estimation.gif "PoseNet Example running on TF JS")

### Roles
Both Zhenning and Vijay have extensive experience in both Python and C++ as well as experience in other applications of Tensorflow that could help in implementing the models needed for pose estimation. Due to this, we can swap responsibilities with regarding implementing both the GUI-logic and other main components of the software. Regardless, for the sake of simplicity, we are planning on having Zhenning work on implementing the main portions of the GUI/UX as well as help with the logic required in determining the “correctness” of a movement. Vijay will be mainly focusing on getting the GUI interconnected with a pose estimation model, contribute towards the aforementioned logic, and refining the GUI styling. 

### Project Management
> **Week**
    **1:** Setup the Qt project and have all the prerequisites installed
    **2:** Find and test out the fastest public version of PoseNet and OpenPose
    **3:** Start writing the algorithm to determine a good movement setup for one exercise; Start building GUI at the same time; **Complete iteration 1 status report**
    **4:** Continue building GUI and the pose estimation logic; Look to implement other more specific estimation models (hand position estimation, feet position, etc.)
    **5:** Extend pose estimation logic to other types of exercises; **Complete iteration 2 status report**
    **6:** Refine GUI elements to look sleek and modern; Run through the flow of the application
    **7:** Complete intended goals and work on resolving any bugs or UX issues
    **8:** **Create a project report and continue debugging the application**
    **9:** **Present project to class**

### Schedule
Our current goal seems quite daunting, but we believe our prior experience will let us complete such a goal within the end of the semester. We plan on meeting at least 3x a week.

### Constraints
The main constraint will be the performance of the pose estimation. We need to strike a good balance between the speed of the pose estimation processing and the accuracy of it.

### Resources
Due to the nature of the application, no external sensors or hardware will be required other than a web camera and a laptop/desktop. As for the installation process, frameworks like Qt and Tensorflow allow developers to package and deploy their application into a simple executable, so the customer will not have to go through any lengthy and complicated installation process.

### Descoping
If we cannot complete all of our planned objectives by the halfway mark of the semester, we will consider descoping to only exhibit pose estimation for one exercise or resort to a non-machine learning related process to have something to show.

