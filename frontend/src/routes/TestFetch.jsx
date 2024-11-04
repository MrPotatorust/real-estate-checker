import { useEffect, useState } from "react";
import { testGet } from "../apiCalls";

export default function TestFetch() {
  const [advertisements, setAdvertisements] = useState([]);
  const [site, setSite] = useState([1]);

  useEffect(() => {
    async function promiseResolution() {
      setAdvertisements(await testGet(site));
    }
    promiseResolution();
  }, [site]);

  console.log(advertisements);
  console.log(site);

  const mappedAdvertisements = advertisements.map((advertisement) => (
    <div key={advertisement.id} className="advertisement">
      <h3>
        <a href={advertisement.link}>{advertisement.title}</a>
      </h3>
      <img src={advertisement.img} alt="advertisement image" />
      <p>{advertisement.price}</p>
      <p>{}</p>
    </div>
  ));
  return (
    <div>
      <select
        name="site_select"
        id="site_select"
        onChange={(e) => setSite(() => e.target.value)}
      >
        <option value="1">1</option>
        <option value="2">2</option>
      </select>
      <h2>NOOOOO</h2>
      {mappedAdvertisements}
    </div>
  );
}
