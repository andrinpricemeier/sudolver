import styles from "./styles/output_tailwind.css";
import type { LinksFunction, MetaFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import {
  Links,
  LiveReload,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
  useLoaderData,
} from "@remix-run/react";

export async function loader() {
  return json({
    ENV: {
      SUDOLVER_API_KEY: process.env.SUDOLVER_API_KEY,
    },
  });
}

export const meta: MetaFunction = () => ({
  charset: "utf-8",
  title: "Sudolver",
  description: "Solve any sudoku by simply taking a picture with your camera.",
  viewport: "width=device-width,initial-scale=1",
  "msapplication-TileColor": "#3497c6",
  "theme-color": "#ffffff",
});

export const links: LinksFunction = () => {
  return [
    { rel: "stylesheet", href: styles },
    {
      rel: "apple-touch-icon",
      href: "/apple-touch-icon.png",
      sizes: "180x180",
    },
    {
      rel: "icon",
      href: "/sudolver_logo.svg",
      type: "image/svg+xml",
    },
    {
      rel: "icon",
      href: "/favicon-32x32.png",
      type: "image/png",
      sizes: "32x32",
    },
    {
      rel: "icon",
      href: "/favicon-16x16.png",
      type: "image/png",
      sizes: "16x16",
    },
    {
      rel: "manifest",
      href: "/site.webmanifest",
    },
    {
      rel: "mask-icon",
      href: "/safari-pinned-tab.svg",
      color: "#3497c6",
    },
    {
      rel: "apple-touch-icon",
      href: "/apple-touch-icon.png",
      sizes: "180x180",
    },
  ];
};

export default function App() {
  const data = useLoaderData();
  return (
    <html lang="en" className="h-full">
      <head>
        <Meta />
        <Links />
      </head>
      <body className="h-full">
        <Outlet />
        <ScrollRestoration />
        <script
          dangerouslySetInnerHTML={{
            __html: `window.ENV = ${JSON.stringify(data.ENV)}`,
          }}
        />
        <script
          defer
          data-domain="sudolver.app"
          src="https://plausible.io/js/plausible.js"
        />
        <Scripts />
        <LiveReload />
      </body>
    </html>
  );
}
