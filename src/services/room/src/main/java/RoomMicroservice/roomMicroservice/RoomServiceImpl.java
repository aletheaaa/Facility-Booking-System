package RoomMicroservice.roomMicroservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Objects;

@Service
public class RoomServiceImpl implements RoomService {
    @Autowired
    private RoomRepository roomRepository;

//    @Override
    public Room saveRoom(Room room) {
        return roomRepository.save(room);
    }

//    @Override
    public List<Room> fetchRoomList() {
        return (List<Room>) roomRepository.findAll();
    }

//    @Override
    public Room updateRoom(Room room, Integer roomId) {
        Room roomDB = roomRepository.findById(roomId).get();

        if (Objects.nonNull(room.getRoomName()) && !"".equalsIgnoreCase(room.getRoomName())) {
            roomDB.setRoomName(room.getRoomName());
        }
        if (Objects.nonNull(room.getRoomType()) && !"".equalsIgnoreCase(room.getRoomType())) {
            roomDB.setRoomType(room.getRoomType());
        }
        if (Objects.nonNull(room.getLocation()) && !"".equalsIgnoreCase(room.getLocation())) {
            roomDB.setLocation(room.getLocation());
        }
        if (Objects.nonNull(room.getCapacity())) {
            roomDB.setCapacity(room.getCapacity());
        }
        if (Objects.nonNull(room.getCost())) {
            roomDB.setCost(room.getCost());
        }
        if (Objects.nonNull(room.getMaxCoBooker())) {
            roomDB.setMaxCoBooker(room.getMaxCoBooker());
        }

        return roomRepository.save(roomDB);
    }

    // delete operation
//    @Override
    public void deleteRoomById(Integer roomId) {
        roomRepository.deleteById(roomId);
    }
}
