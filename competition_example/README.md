This is a robot that must stay in the "road". The road width is delimited by two parallel white lines, anything in the middle is considered being inside the road. Here are conditions that must be met:
Considerations:
- The color of the edge lines for the road is white. A range of color that defines that should be stored in a variable # This is for the HSV or RGB camera color. Not limit sensors
- The color of the road itself. A range of color that defines that should be stored in a variable # This if for the HSV or RGB camera color. Not limit sensors
- The frame of the camera that will serve as input for the computer vision. Example: if the image is 1920x1080, but the user only wants to use the lower part of the image for any analysis for the robot to make, a variable must be declared which defines the section of the frame that will be used


- The robot must move forward
- Grayscale sensors must detect the "edge" of either side of the road. If the left sensor is triggered; then it means the robot is about to leave the road by the left side. In order to prevent that, the robot must turn right. If the right sensor is triggered; then it means the robot is about to leave the road by the right side. In order to prevent that, make the robot turn left.
    -Using the camera to detect the parallel lines that define the "road". A simple calculation must be made in order to define the center of the road. Then steer in order to make sure the robot keeps itself in the middle of the road as best as possible (implement a PID controller for that)
    - If the ultrasonic sensor detects an obstacle which can be defined as any measurement below x distance. The robot should:
        - identify the color of the object. (Anything that is not in range of the color of the edge lines or the road itself.)
        - Calculate the objects centroid
        - compare the distance in pixels between the centroid of the calculated object and each of the road's edge lines. (make it so the robot steer in the direction where there's more space to go through)