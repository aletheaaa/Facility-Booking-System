package RoomMicroservice.roomMicroservice;


import org.springframework.stereotype.Service;

import java.util.List;

public interface RoomService {
    // save
    Room saveRoom(Room room);

    // read
    List<Room> fetchRoomList();

    // update
    Room updateRoom(Room room, Integer roomId);

    // delete
    void deleteRoomById(Integer roomId);
}
