def check_permissions():
    print("This program will try to get the required permissions from your operating system.\n")
    print("Please grant all the requested permissions, and restart this program")
    print("until no further permission request is asked.\n")
    # print("Press ENTER to continue")
    # input()

    print("\n1 of 3: Writing data on disk")
    from . import models

    print("2 of 3: Recording screen content")
    from . import video
    video.check_video_permissions()

    print("3 of 3: Recording webcam")
    from . import webcam
    webcam.check_webcam_permissions()

    print("\nPermission check completed!")
