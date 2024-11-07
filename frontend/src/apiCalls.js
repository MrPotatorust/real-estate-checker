export async function testGet(site) {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/test_get/${site}`);
    const data = await res.json();
    return data;
  } catch (error) {
    return `Error fetching from api error: ${error}`;
  }
}
