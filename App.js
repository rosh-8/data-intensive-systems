import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {
  const [db, setDb] = useState("students");
  const [data, setData] = useState([]);
  const [field1, setField1] = useState("");
  const [field2, setField2] = useState("");

  const loadData = async () => {
    const res = await axios.get(`http://localhost:5000/data/${db}`);
    setData(res.data);
  };

  useEffect(() => { loadData(); }, [db]);

  const addRecord = async () => {
    let payload = {};
    if (db === 'students') payload = { name: field1, course: field2 };
    if (db === 'books') payload = { title: field1, author: field2 };
    if (db === 'employees') payload = { name: field1, department: field2 };

    await axios.post(`http://localhost:5000/data/${db}`, payload);
    setField1('');
    setField2('');
    loadData();
  };

  return (
    <div style={{padding:'20px'}}>
      <h1>Database Manager</h1>
      <select value={db} onChange={(e)=>setDb(e.target.value)}>
        <option value='students'>Students</option>
        <option value='books'>Books</option>
        <option value='employees'>Employees</option>
      </select>
      <br/><br/>
      <input placeholder='Field 1' value={field1} onChange={(e)=>setField1(e.target.value)} />
      <input placeholder='Field 2' value={field2} onChange={(e)=>setField2(e.target.value)} />
      <button onClick={addRecord}>Add</button>
      <ul>
        {data.map((row)=><li key={row.id}>{JSON.stringify(row)}</li>)}
      </ul>
    </div>
  );
}
