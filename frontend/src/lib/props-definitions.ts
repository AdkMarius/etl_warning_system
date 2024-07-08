import React from "react";
import {DataModel} from "@/lib/datas-definition";

export type H2HeadingProps = {
    children: string;
}

export type dType = "diseases" | "dataElements" | "indicators";

export type SearchBarProps = {
    dType: dType;
    placeholder: string;
    searchValue: string;
    handleSearchValue: (e: React.ChangeEvent<HTMLInputElement>) => void;
    filterType?: string;
    handleSelectFilterType?: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

export type TableProps = {
    dType: dType;
    placeholder: string;
    status: string;
    headingChildren: string;
    selectedItem: DataModel;
    handleClick: (item: DataModel) => void;
}

export type FetchDataProps = {
    page: number | string;
    query: string;
    filterType?: string;
    url: string;
}