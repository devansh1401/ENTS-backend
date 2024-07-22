import { useQuery, useMutation, useQueryClient} from '@tanstack/react-query';
import axios from 'axios';

export const getCellData = (cellIds, resample, startTime, endTime) => {
  return axios
    .get(
      `${
        process.env.PUBLIC_URL
      }/api/cell/datas?cellIds=${cellIds.toString()}&resample=${resample}&startTime=${startTime.toHTTP()}&endTime=${endTime.toHTTP()}`, 
    )
    .then((res) => res.data);
};

export const getCells = () => {
  return axios.get(`${process.env.PUBLIC_URL}/api/cell/id`).then((res) => res.data);
};

export const addCell = (cellName, location, longitude, latitude, archive, email) => {
  return axios
    .post(`${process.env.PUBLIC_URL}/api/cell/`, {
      name: cellName,
      location: location,
      longitude: longitude,
      latitude: latitude,
      archive: archive,
      userEmail: email 
      // this doesn't a 1 to 1 mapping with models, 
      // just make sure that the message structure (http request) is the same with the frontend and the backend
      // by the same, I mean, the both the frontend and the backend agree on the structure (schema)
    })
    .then((res) => res.data)
    .catch((error) => {
      console.log(error);
    });
};

export const useCells = () =>
  useQuery({
    queryKey: ['cell info'],
    queryFn: () => getCells(),
    refetchOnWindowFocus: false,
  });

  export const setCellArchive = async (cellId, archive) => {
    const url = `${process.env.PUBLIC_URL}/api/cell/${cellId}`;
    try {
      const response = await axios.put(
        url,
        { archive },
        { headers: { 'Content-Type': 'application/json' } }
      );
      return response.data;
    } catch (error) {
      console.error('Error setting cell archive:', error.response ? error.response.data : error.message);
      throw error;
    }
  };
  
  export const useSetCellArchive = () => {
    const queryClient = useQueryClient();
    return useMutation({
      mutationFn: ({ cellId, archive }) => setCellArchive(cellId, archive),
      onSuccess: () => {
        // Invalidate or refetch the cells query to get updated data
        queryClient.invalidateQueries(['cell info']);
      },
      onError: (error) => {
        console.error('Error setting cell archive:', error);
      },
    });
  };
  
export const pollCellDataResult = (taskId) =>{
  return axios
  .get(
    `${
      process.env.PUBLIC_URL
    }/api/status/${taskId}`
  )
  .then((res) => {
      return res.data; 
  });
}
