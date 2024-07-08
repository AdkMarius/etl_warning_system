'use client';

import React, {useEffect, useState} from "react";
import {useDebounce} from "use-debounce";
import {DataSkeletons, H2Heading, TableData, SearchBar} from "@/components";
import {DataModel, DataResponse} from "@/lib/datas-definition";
import {Pagination} from "@mui/material";
import {FetchDataProps, TableProps} from "@/lib/props-definitions";

const fetchFromAPI = async (props: FetchDataProps) => {
    const {
        page,
        query,
        filterType,
        url,
    } = props;

    const obj = {
        page: page,
        query: query,
        filterType: filterType
    }

    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(obj)
        });
        return res.json();
    } catch (error) {
        console.error("API Error", error);
        throw new Error("Error while fetching data.")
    }
}

function Table(props: TableProps) {
    const initialData: DataResponse = {
        dataElements: [],
        pager: {
            page: 1,
            pageCount: 0,
            nextPage: 0,
            pageSize: 0,
            total: 0
        }
    };

    const {
        dType,
        placeholder,
        status,
        headingChildren,
        selectedItem,
        handleClick
    } = props;

    const [page, setPage] = useState<number>(1);

    const [query, setQuery] = useState<string>("");

    const [debouncedQuery] = useDebounce(query, 1000);

    const [filterType, setFilterType] = useState<string>("name");

    const [loading, setLoading] = useState<boolean>(false);

    const [data, setData] = useState<DataResponse>(initialData);

    const handlePageChange = (_e: React.ChangeEvent<unknown>, page: number) => {
        setPage(page);
    };

    const handleSelectFilterType = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setFilterType(e.target.value);
    };

    const handleSearchValue = (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value);
    };

    useEffect(() => {
        let ignore = false;

        (async () => {
            let dataResponse: DataResponse;

            setLoading(true);
            try {
                if (dType === "diseases") {
                    dataResponse = await fetchFromAPI({
                        url: '/api/get-diseases',
                        page: page,
                        query: debouncedQuery,
                        filterType: filterType
                    })
                } else if (dType === "indicators") {
                    dataResponse = await fetchFromAPI({
                        url: '/api/get-indicators',
                        page: page,
                        query: debouncedQuery
                    })
                } else if (dType === "dataElements") {
                    dataResponse = await fetchFromAPI({
                        url: '/api/get-data-elements',
                        page: page,
                        query: debouncedQuery,
                    })
                }
                if (!ignore) {
                    setData(prevState => ({
                        ...prevState,
                        dataElements: dataResponse.dataElements,
                        pager: {
                            page: dataResponse.pager.page,
                            pageSize: dataResponse.pager.pageSize,
                            pageCount: dataResponse.pager.pageCount,
                            total: dataResponse.pager.total,
                            nextPage: dataResponse.pager.nextPage
                        }
                    }));
                }
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                if (!ignore) {
                    setLoading(false);
                }
            }
        })();


        return () => {
            ignore = true;
        };
    }, [page, debouncedQuery]);

    return (
        <article className="flex flex-col w-2/6">
            { dType === "diseases" ? (
                <SearchBar
                    key={dType}
                    dType={dType}
                    placeholder={placeholder}
                    searchValue={query}
                    handleSearchValue={handleSearchValue}
                    filterType={filterType}
                    handleSelectFilterType={handleSelectFilterType}
                />
            ) : (
                <SearchBar
                    key={dType}
                    dType={dType}
                    placeholder={placeholder}
                    searchValue={query}
                    handleSearchValue={handleSearchValue}
                />
            )}

            <div className="flex flex-col w-full max-h-[500px] overflow-y-scroll shadow-md bg-white my-4">
                <div className="p-4">
                    <H2Heading>{headingChildren}</H2Heading>
                </div>

                {loading ? (
                    <DataSkeletons/>
                ) : (
                    <TableData
                        key={dType}
                        items={data.dataElements}
                        status={status}
                        selectedItem={selectedItem}
                        handleClick={handleClick}
                    />
                )}

                <div className="flex justify-center mt-auto p-4">
                    <Pagination
                        key={dType}
                        count={data.pager.pageCount}
                        page={page}
                        onChange={handlePageChange}
                        color="primary"
                    />
                </div>
            </div>
        </article>
    );
}

export default Table;