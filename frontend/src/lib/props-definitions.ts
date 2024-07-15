import React from "react";
import {DataModel} from "@/lib/datas-definition";

export type H2HeadingProps = {
    children: string;
}

export type dType = "diseases" | "dataElements" | "indicators";

export type ErrorType = 'empty' | 'submitting' | 'success' | 'error';

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

export type SubmitResponse = {
    httpStatus: string;
    httpStatusCode: number;
    message: string;
}

export type TableDataProps = {
    status: string;
    items: DataModel[];
    selectedItem: DataModel;
    handleClick: (item: DataModel) => void;
}

export type ButtonProps = {
    buttonText: string;
    handleClick: () => void;
}