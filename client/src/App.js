import React, {useState,useEffect} from 'react';

function App() {

  const [data,setData] = useState();

  useEffect(() => {
    const getUsers = async () => {
      const users = await fetch("/home");
      console.log(users);
      // console.log(data)
}
getUsers();
},[]);



}

export default App;