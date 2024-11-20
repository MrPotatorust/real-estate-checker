import { useEffect, useState } from "react";
import { testGet } from "../apiCalls";

export default function TestFetch() {
  const [advertisements, setAdvertisements] = useState([]);
  const [lookupField, setLookupFields] = useState({
    site_select: "1",
    lookup_word: "",
    slider: "",
  });

  let mappedAdvertisements;

  async function promiseResolution() {
    setAdvertisements(
      await testGet(lookupField.site_select, lookupField.lookup_word)
    );
  }

  function handleChange(e) {
    let { name, value } = e.target;
    setLookupFields((adverts) => {
      return { ...adverts, [name]: value };
    });
  }

  useEffect(() => {
    promiseResolution();
  }, []);

  mappedAdvertisements = advertisements.map((advertisement) => (
    <div key={advertisement.id} className="advertisement">
      <h3>
        <a href={advertisement.link}>{advertisement.title}</a>
      </h3>
      <img src={advertisement.img} alt="advertisement image" />
      <p>{advertisement.price}</p>
    </div>
  ));

  return (
    <div className="container">
      <div className="filter-fetch">
        <form>
          <input
            type="text"
            name="lookup_word"
            value={lookupField.lookup_word}
            onChange={(e) => handleChange(e)}
          />
          <select
            name="site_select"
            id="site_select"
            value={lookupField.site_select}
            onChange={(e) => handleChange(e)}
          >
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
          <button type="button" onClick={promiseResolution}>
            Refresh
          </button>
        </form>
        <div class="slidecontainer">
          <input
            type="range"
            min="1"
            max="100"
            className="slider"
            id="myRange"
            name="slider"
            value={lookupField.slider}
            onChange={handleChange}
          />
        </div>
      </div>
      <h2>Advertisements</h2>
      {mappedAdvertisements.length > 0 ? (
        mappedAdvertisements
      ) : (
        <p>Nothing to find</p>
      )}
    </div>
  );
}
