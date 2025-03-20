from ksrtc.models import BusTrip
from ksrtc.serializer import BusTripSerializer, UserSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User

class KsrtcTripViewSet(viewsets.ModelViewSet):
    queryset = BusTrip.objects.all()
    serializer_class = BusTripSerializer
    
    def get_queryset(self):
        """Return all trips (or only the logged-in user's trips)."""
        if self.request.user.is_authenticated:
            return BusTrip.objects.filter(user=self.request.user)
        return BusTrip.objects.all()  # Return no trips for unauthenticated users
    
    def list(self, request, *args, **kwargs):
        """Return trips based on optional source & destination filters (case-insensitive)."""
        source = request.query_params.get("source")
        destination = request.query_params.get("destination")
        
        # Convert inputs to lowercase if provided
        source = source.lower() if source else None
        destination = destination.lower() if destination else None
        
        # Get user-specific trips
        bus_trips = self.get_queryset()
        
        # Apply filters if provided
        if source or destination:
            filtered_bus_trips = []
            for bus_trip in bus_trips:
                stations = bus_trip.stations  # JSONField (List of dicts)
                # Convert station names to lowercase for case-insensitive matching
                stations_lower = [{**s, "station": s["station"].lower()} for s in stations]
                
                # Get index positions of source and destination
                source_index = next((i for i, s in enumerate(stations_lower) if s["station"] == source), None)
                destination_index = next((i for i, s in enumerate(stations_lower) if s["station"] == destination), None)
                
                if source and destination:
                    if source_index is not None and destination_index is not None and destination_index > source_index:
                        filtered_bus_trips.append(bus_trip)
                elif source and source_index is not None:
                    filtered_bus_trips.append(bus_trip)
                elif destination and destination_index is not None:
                    filtered_bus_trips.append(bus_trip)
            
            bus_trips = filtered_bus_trips  # Apply filtered results
        
        serializer = self.get_serializer(bus_trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['GET'])
    def me(self, request):
        """
        Return the authenticated user's details
        Endpoint: /api/user/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)