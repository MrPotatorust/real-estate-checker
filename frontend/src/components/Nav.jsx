import { Link } from "react-router-dom";

export default function Nav() {
  return (
    <nav>
      <ul className="nav--ul list">
        <li>
          <h3 className="nav--heading">
            <Link to={""}>Domov</Link>
          </h3>
        </li>
        <li>
          <h3 className="nav--heading">
            <Link to={"nehnutelnosti"}>Nehnutelnosti</Link>
          </h3>
        </li>
        <li>
          <h3 className="nav--heading">
            <Link to={"bazos"}>Bazos</Link>
          </h3>
        </li>
        <li>
          <h3 className="nav--heading">
            <Link to={"about-us"}>Kto sme?</Link>
          </h3>
        </li>
        <li>
          <h3 className="nav--heading">
            <Link to={"test-fetch"}>test</Link>
          </h3>
        </li>
      </ul>
    </nav>
  );
}
