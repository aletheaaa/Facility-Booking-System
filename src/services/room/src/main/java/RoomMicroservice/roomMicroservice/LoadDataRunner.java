package RoomMicroservice.roomMicroservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

@Component
public class LoadDataRunner implements ApplicationRunner {
    @Autowired
    private RoomRepository roomRepository;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        Room GroupStudyRoom = new Room();
        GroupStudyRoom.setRoomName("SOE GSR 3-1");
        GroupStudyRoom.setRoomType("Group Study Room");
        GroupStudyRoom.setLocation("School of Economics");
        GroupStudyRoom.setCapacity(6);
        GroupStudyRoom.setCost(40);
        GroupStudyRoom.setMaxCoBooker(2);

        Room GroupStudyRoom2 = new Room();
        GroupStudyRoom2.setRoomName("SOA GSR 2-2");
        GroupStudyRoom2.setRoomType("Group Study Room");
        GroupStudyRoom2.setLocation("School of Accountancy");
        GroupStudyRoom2.setCapacity(6);
        GroupStudyRoom2.setCost(40);
        GroupStudyRoom2.setMaxCoBooker(2);

        Room SeminarRoom = new Room();
        SeminarRoom.setRoomName("SOE SR 2-2");
        SeminarRoom.setRoomType("Seminar Room");
        SeminarRoom.setLocation("School of Economics");
        SeminarRoom.setCapacity(40);
        SeminarRoom.setCost(100);
        SeminarRoom.setMaxCoBooker(3);

        Room SeminarRoom2 = new Room();
        SeminarRoom2.setRoomName("SOA SR 3-2");
        SeminarRoom2.setRoomType("Seminar Room");
        SeminarRoom2.setLocation("School of Accountancy");
        SeminarRoom2.setCapacity(40);
        SeminarRoom2.setCost(100);
        SeminarRoom2.setMaxCoBooker(3);

        roomRepository.save(GroupStudyRoom);
        roomRepository.save(GroupStudyRoom2);
        roomRepository.save(SeminarRoom);
        roomRepository.save(SeminarRoom2);
    }
}
