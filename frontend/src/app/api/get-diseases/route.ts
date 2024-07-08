import { NextRequest, NextResponse} from "next/server";
import {fetchFilteredDiseases} from "@/lib/datas";
import {DataResponse} from "@/lib/datas-definition";

export const dynamic = 'force-dynamic'

export async function POST(request: NextRequest) {
    const data = await request.json()

    const dataResponse: DataResponse = await fetchFilteredDiseases(data.page, data.query, data.filterType);

    return NextResponse.json(dataResponse);
}