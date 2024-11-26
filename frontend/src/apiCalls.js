export async function testGet(formData) {
  if (formData.lookup_word == ""){
    lookup_word = '%$*any'
  }
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/api/test_get/site=${formData.site}/lookup-word=${formData.lookup_word}/min-price=${formData.minPrice}/max-price=${formData.maxPrice}`
    );
    const data = await res.json();
    return data;
  } catch (error) {
    return `Error fetching from api error: ${error}`;
  }
}