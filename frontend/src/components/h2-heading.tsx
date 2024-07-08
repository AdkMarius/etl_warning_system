import { H2HeadingProps } from "@/lib/props-definitions";

function H2Heading({ children }: H2HeadingProps) {
    return <h2 className="text-black text-m-24 font-medium">{children}</h2>
}

export default H2Heading;