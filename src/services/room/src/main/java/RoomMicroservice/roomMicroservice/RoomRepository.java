package RoomMicroservice.roomMicroservice;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RoomRepository extends CrudRepository<Room, Integer> {

    @Query(value = "SELECT * FROM room r WHERE r.location IN :location", nativeQuery = true)
    List<Room> findRoomsByLocation(List<String> location);

    @Query(value = "SELECT * FROM room r WHERE r.room_type IN :roomType", nativeQuery = true)
    List<Room> findRoomsByRoomType(List<String> roomType);

    @Query(value = "SELECT * FROM room r WHERE r.room_type IN :roomType AND r.location IN :location", nativeQuery = true)
    List<Room> findRoomsByRoomTypeAndCapacity(List<String> roomType, List<String> location);
}
