'use client';

import React from "react";
import {SearchBarProps} from "@/lib/props-definitions";

function SearchBar(props: SearchBarProps) {
    const {
        dType,
        placeholder,
        searchValue,
        handleSearchValue,
        filterType,
        handleSelectFilterType
    } = props;

    return (
        <div className="flex flex-row h-[100px] w-full gap-x-3">
            <input
                type="search"
                className="text-black w-4/6 h-[50px] border bg-white rounded-lg focus:border-primary-3
                      caret-primary-3 focus:outline-none px-2"
                placeholder={placeholder}
                value={searchValue}
                onChange={handleSearchValue}
            />

            {dType === "diseases" && (
                <select
                    className="text-black w-2/6 h-[50px] border bg-white rounded-lg focus:border-primary-3
                    caret-primary-3 focus:outline-none px-2"
                    value={filterType}
                    onChange={handleSelectFilterType}
                >
                    <option value="name">Name</option>
                    <option value="code">Code</option>
                </select>
            )}

        </div>
    );
}

export default SearchBar;