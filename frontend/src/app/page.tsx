import type {Metadata} from "next";
import {ContainerTable} from "@/components";
import React from "react";


export const metadata: Metadata = {
  title: "Early Warning System",
  description: "ETL System - Integration of GNUHealth in DHIS2",
};

export default function Page() {
  return (
    <main className="flex flex-col justify-center w-full p-8 gap-y-10">
      <ContainerTable />
    </main>
  );
}
1