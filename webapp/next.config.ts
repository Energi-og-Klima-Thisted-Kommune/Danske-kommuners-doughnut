import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  output: "export",
  // GitHub Pages: sitet ligger under /<repo>/, indtil det får eget domæne.
  // Workflowen sætter NEXT_BASE_PATH ud fra Pages-opsætningen (tom ved eget
  // domæne), så koden skal ikke rettes, når domænet skifter. Links skal derfor
  // gå gennem next/link, ikke <a href="/...">, ellers mangler stien.
  basePath: process.env.NEXT_BASE_PATH || "",
  // Next lægger både side.html og en mappe side/ i output. Pages svarer 404 på
  // /side, når der findes en mappe uden index.html, så hver side skal være
  // side/index.html.
  trailingSlash: true,
  // Roden er repoets rod, ikke webapp/: shared.ts importerer
  // data/indikatorer.json, som Python-pipelinen også læser. Med webapp/ som
  // rod nægter Turbopack at resolve filer uden for mappen.
  turbopack: {
    root: path.resolve(__dirname, ".."),
  },
  allowedDevOrigins: ["127.0.0.1"],
};

export default nextConfig;
