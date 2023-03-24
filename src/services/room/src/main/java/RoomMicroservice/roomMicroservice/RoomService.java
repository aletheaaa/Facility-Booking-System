package RoomMicroservice.roomMicroservice;


import net.minidev.json.JSONObject;
import org.springframework.stereotype.Service;

import java.util.List;

public interface RoomService {
    // save
    Room saveRoom(Room room);

    // read
    List<Room> fetchRoomList();

    // reading specific rooms by roomType
    List<Room> fetchRoomByRoomType(List roomType);

    // reading specific rooms by location
    List<Room> fetchRoomByLocation(List location);

    // reading specific rooms by location
    List<Room> fetchRoomByRoomTypeAndLocation(List<String> roomType, List<String> location);

    // update
    Room updateRoom(Room room, Integer roomId);

    // delete
    void deleteRoomById(Integer roomId);
}
