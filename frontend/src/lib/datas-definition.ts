export type DataModel = {
    id: string;
    code?: string;
    displayName: string;
}

export type DataResponse = {
    dataElements: DataModel[],
    pager: {
        nextPage: number,
        page: number,
        pageCount: number,
        pageSize: number,
        total: number
    }
}

export type SelectedData = {
    disease: {
        id: string;
        code: string;
        displayName: string;
    },
    indicator: {
        id: string;
        displayName: string;
    },
    dataElement: {
        id: string;
        displayName: string;
    }
};