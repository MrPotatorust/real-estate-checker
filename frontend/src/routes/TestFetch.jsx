import { useEffect, useState } from "react";
import { testGet } from "../apiCalls";

export default function TestFetch() {
  const [advertisements, setAdvertisements] = useState([]);
  const [lookupField, setLookupFields] = useState({
    siteSelect: "1",
    lookupWord: "",
    slider: "",
    minPrice: "",
    maxPrice: "",
  });

  let mappedAdvertisements;

  async function promiseResolution() {
    setAdvertisements(await testGet(lookupField));
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

  console.log(lookupField.slider);

  return (
    <div className="container">
      <div className="filter-fetch">
        <form>
          <label>
            Lookup word
            <input
              type="text"
              name="lookupWord"
              value={lookupField.lookup_word}
              onChange={(e) => handleChange(e)}
            />
          </label>
          <label>
            Minimum price
            <input
              type="text"
              name="minPrice"
              value={lookupField.minimum_price}
              onChange={(e) => handleChange(e)}
            />
          </label>
          <label>
            Maximum price
            <input
              type="text"
              name="maxPrice"
              value={lookupField.maximum_price}
              onChange={(e) => handleChange(e)}
            />
          </label>
          <select
            name="siteSelect"
            id="site-select"
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
