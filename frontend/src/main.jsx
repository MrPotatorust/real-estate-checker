import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Root from "./routes/root.jsx";
import ErrorPage from "./error-page.jsx";
import HomePage from "./routes/HomePage.jsx";
import AboutUs from "./routes/AboutUs.jsx";
import Bazos from "./routes/Bazos.jsx";
import Nehnutelnosti from "./routes/Nehnutelnosti.jsx";
import TestFetch from "./routes/TestFetch.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./css/normalize.css";
import "./css/index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
        element: <HomePage />,
      },
      {
        path: "about-us",
        element: <AboutUs />,
      },
      {
        path: "nehnutelnosti",
        element: <Nehnutelnosti />,
      },
      {
        path: "bazos",
        element: <Bazos />,
      },
      {
        path: "test-fetch",
        element: <TestFetch />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
