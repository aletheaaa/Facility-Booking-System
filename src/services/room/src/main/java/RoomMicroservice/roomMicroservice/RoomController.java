package RoomMicroservice.roomMicroservice;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@RestController
public class RoomController {
    private RoomRepository roomRepository;

    @Autowired private RoomService roomService;

//    public RoomController(RoomRepository roomRepository) {
//        this.roomRepository = roomRepository;
//    }

    // getting all the books
    // Save operation
    @PostMapping("/rooms")
    public Room saveRoom(
            @Valid @RequestBody Room room)
    {
        return roomService.saveRoom(room);
    }

    // Read operation
    @GetMapping("/rooms")
    public List<Room> fetchRoomList()
    {
        return roomService.fetchRoomList();
    }

    // Update operation
    @PutMapping("/rooms/{id}")
    public Room
    updateRoom(@RequestBody Room room,
                     @PathVariable("id") Integer roomId)
    {

        return roomService.updateRoom(
                room, roomId);
    }

    // Delete operation
    @DeleteMapping("/rooms/{id}")
    public String deleteRoomById(@PathVariable("id") Integer roomId)
    {
        roomService.deleteRoomById(
                roomId);
        return "Deleted Successfully";
    }
}
