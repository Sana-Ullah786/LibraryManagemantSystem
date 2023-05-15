import { ReactElement } from "react";
import { Link } from "react-router-dom";

/**
 * The properties passed for this page
 */
interface LibrarianLinksProps {
    url: string;
}


/**
 * This component returns the links for updating and creating books.
 * @param props The properties required for forming the correct link
 * @returns A component containing links
 */
function LibrarianLinks(props: LibrarianLinksProps): ReactElement {
    return (
        <>
            <Link to={`${props.url}/update`} style={{ color: 'orange' }}> Update </Link>
            <Link to={`${props.url}/delete`} style={{ color: 'red' }}> Delete </Link>
        </>
    )
}

export default LibrarianLinks;
