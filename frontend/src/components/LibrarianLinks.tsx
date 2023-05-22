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
        <div className="genre-list-item-buttons">
            <Link to={`${props.url}/update`}className="genre-list-update-button"> Update </Link>
            <Link to={`${props.url}/delete`} className="genre-list-delete-button"> Delete </Link>
        </div>
    )
}

export default LibrarianLinks;
