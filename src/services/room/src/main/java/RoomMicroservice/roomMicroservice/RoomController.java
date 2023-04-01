package RoomMicroservice.roomMicroservice;

import com.fasterxml.jackson.databind.JsonSerializer;
import com.sun.net.httpserver.Authenticator;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Null;
import net.minidev.json.JSONArray;
import net.minidev.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.lang.reflect.Type;
import java.util.List;


@RestController
public class RoomController {
    private RoomRepository roomRepository;

    @Autowired private RoomService roomService;

//    public RoomController(RoomRepository roomRepository) {
//        this.roomRepository = roomRepository;
//    }

    // Save operation
    @PostMapping("/rooms")
    public JSONObject saveRoom(
            @Valid @RequestBody Room room)
    {
        // checking that all the relevant fields are there
        if (room.getRoomName() == null || room.getRoomType() == null || room.getLocation() == null || room.getCapacity() == null || room.getCost() == null || room.getMaxCoBooker() == null){
            JSONObject failureJsonObject = new JSONObject();
            failureJsonObject.put("code", 400);
            failureJsonObject.put("message", "Please provide all the required fields: roomName, roomType, location, capacity, cost or MaxCoBooker.");
            return failureJsonObject;
        }

        JSONObject successJsonObject = new JSONObject();
        successJsonObject.put("code", 200);
        successJsonObject.put("data", roomService.saveRoom(room));
        successJsonObject.put("message", "Successfully updated room details");
        return successJsonObject;
    }

    // Read operation
    @CrossOrigin
    @GetMapping("/rooms")
    public JSONObject fetchRoomList()
    {
        JSONObject successJsonObject = new JSONObject();
        successJsonObject.put("code", 200);
        successJsonObject.put("data", roomService.fetchRoomList());
        successJsonObject.put("message", "Successfully retrieved the rooms");
        return successJsonObject;
    }

    // get the room with the selected fields
    @GetMapping("/rooms/getSpecificRooms")
    public JSONObject fetchSpecificRoomList(@RequestBody UserFields body){
        JSONObject successJsonObject = new JSONObject();
        if (!body.getLocation().isEmpty() && !body.getRoomType().isEmpty()){
            successJsonObject.put("data", roomService.fetchRoomByRoomTypeAndLocation(body.getRoomType(), body.getLocation()));
        } else if (body.getRoomType().isEmpty()) {
            successJsonObject.put("data", roomService.fetchRoomByLocation(body.getLocation()));
        } else {
            successJsonObject.put("data", roomService.fetchRoomByRoomType(body.getRoomType()));
        }

        successJsonObject.put("code", 200);
        successJsonObject.put("message", "Successfully retrieved the rooms");
        return successJsonObject;
    }

    // Update operation
    @PutMapping("/rooms/{id}")
    public JSONObject
    updateRoom(@RequestBody Room room,
                     @PathVariable("id") Integer roomId)
    {
        // checking for relevant fields
        if (room.getRoomName() == null && room.getRoomType() == null && room.getLocation() == null && room.getCapacity() == null && room.getCost() == null && room.getMaxCoBooker() == null){
            JSONObject failureJsonObject = new JSONObject();
            failureJsonObject.put("code", 400);
            failureJsonObject.put("message", "Please input at least one field to update: roomName, roomType, location, capacity, cost or MaxCoBooker.");
            return failureJsonObject;
        }

        JSONObject successJsonObject = new JSONObject();
        successJsonObject.put("code", 200);
        successJsonObject.put("data", roomService.updateRoom(room, roomId));
        successJsonObject.put("message", "Successfully updated room details");
        return successJsonObject;
    }

    // Delete operation
    @DeleteMapping("/rooms/{id}")
    public JSONObject deleteRoomById(@PathVariable("id") Integer roomId)
    {
        roomService.deleteRoomById(roomId);
        JSONObject successJsonObject = new JSONObject();
        successJsonObject.put("code", 200);
        successJsonObject.put("message", "Deleted Successfully");
        return successJsonObject;
    }
}
