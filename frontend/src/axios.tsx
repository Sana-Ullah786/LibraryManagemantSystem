import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
import { HomeData } from "./components/pages/Home";
import {
  Book,
  BookSaved,
  Author,
  AuthorDetails,
  Genre,
  Tokens,
  Language,
  ErrorObject,
} from "./CustomTypes";
import jwt_decode from "jwt-decode";
import { DecodedRefreshToken } from "./contexts/AuthContext";

export class APIClient {
  /**
   * This class handles all the calls to the Django Rest Api
   * The class is a singleton, and uses an Axios Instance as an attribute
   */

  private static axiosInstance: AxiosInstance;
  private static instance: APIClient;

  //The constructor creates an axiosInstance
  private constructor(options: AxiosRequestConfig) {
    APIClient.axiosInstance = axios.create(options);
  }

  //The getInstance method returns an instance of the class to be used
  public static getInstance(options: AxiosRequestConfig): APIClient {
    if (!APIClient.instance) {
      APIClient.instance = new APIClient(options);
      APIClient.instance.getInterceptors();
    }
    return APIClient.instance;
  }

  private handleErrors(error: any): ErrorObject | undefined {
    console.log(error);
    if (error.response) {
      const err: ErrorObject = {
        status: error.response.status,
        message: error.response.data.detail,
      };
      return err;
    }
  }

  //This method uses api call to get book details using id. It returns the received details.
  public GetBookDetails(id: string): Promise<BookSaved> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/books/" + id)
        .then((res) => {
          const book: BookSaved = this.bookDeserialize(res.data);
          resolve(book);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method uses book post api to create a new book
  public CreateBook(book: Book): Promise<number> {
    return APIClient.axiosInstance
      .post("/books/", this.bookSerialize(book))
      .then((res) => {
        // An id is assigned to book once its saved in backend server
        const id: number = res.data.id;
        return id;
      });
  }

  // This method uses book put api to edit a book
  public UpdateBook(book: Book, id: number): Promise<boolean> {
    return APIClient.axiosInstance
      .put("/books/" + String(id) + "/", this.bookSerialize(book))
      .then((res) => {
        return true;
      });
  }

  // This method deletes book using delete api for book
  public DeleteBook(id: string): Promise<boolean> {
    return APIClient.axiosInstance.delete("/books/" + id + "/").then((res) => {
      return true;
    });
  }

  // This method converts a Book object from json to Book interface
  private bookDeserialize(json: any): BookSaved {
    let book: BookSaved = json;

    book.authorId = json.author;
    book.languageId = json.language;
    book.genreIds = json.genre;

    return book;
  }

  // This method converts a Book object from json to Book interface
  public bookSerialize(book: Book) {
    let serialized = {
      title: book.title,
      author: book.authorId,
      summary: book.summary,
      isbn: book.isbn,
      language: book.languageId,
      genre: book.genreIds,
    };

    return serialized;
  }

  //This method uses api call to fetch list of books. It returns this list.
  public GetBookList(): Promise<BookSaved[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/books")
        .then((response) => {
          let bookList: BookSaved[] = [];

          for (let data of response.data) {
            bookList.push(this.bookDeserialize(data));
          }

          resolve(bookList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns the genre using its id.
  public GetGenreDetails(id: string): Promise<Genre> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`genres/${id}`)
        .then((res) => {
          const genre: Genre = res.data;
          resolve(genre);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns the all genres.
  public GetAllGenres(): Promise<Genre[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`genres/`)
        .then((res) => {
          const genreList: Genre[] = res.data;
          resolve(genreList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns all languages
  public GetAllLanguages(): Promise<Language[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("languages/")
        .then((res) => {
          const languageList: Language[] = res.data;
          resolve(languageList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method fetches and returns the language using its id.
  public GetLanguageDetails(id: string): Promise<Language> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get(`languages/${id}`)
        .then((res) => {
          const language: Language = res.data;
          resolve(language);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get the detauls of an author
  public GetAuthorDetails(id: string): Promise<Author> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/authors/" + id)
        .then((res) => {
          const author: Author = res.data;
          resolve(author);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  // This method returns all authors using api
  public GetAllAuthors(): Promise<Author[]> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/authors/")
        .then((res) => {
          const authorList: Author[] = res.data;
          resolve(authorList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get data needed to fill the home page
  public GetHomePageData(): Promise<HomeData> {
    return new Promise((resolve, reject) => {
      APIClient.axiosInstance
        .get("/home")
        .then((res) => {
          let HomePageData: HomeData = res.data;
          resolve(HomePageData);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get a list of all the authors
  public GetAuthorsList(): Promise<Author[]> {
    return new Promise((resolve, reject) => {
      let authorList: Author[];
      APIClient.axiosInstance
        .get("/authors")
        .then((response) => {
          authorList = response.data;
          resolve(authorList);
        })
        .catch((error) => {
          reject(APIClient.instance.handleErrors(error));
        });
    });
  }

  //Used to get access and refresh tokens for the login component
  public Login(data: FormData): Promise<Tokens> {
    return APIClient.axiosInstance.post("/auth/token", data).then((res) => {
      let tokens: Tokens = {
        access_token: res.data.token,
        refresh_token: "",
      };
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      APIClient.instance.SetAuthorizationHeaders(
        "Bearer " + tokens.access_token
      );
      return tokens;
    });
  }

  //Used to set the authorization headers with the access token for the axios instant
  private SetAuthorizationHeaders(TokenHeader: String | null): void {
    APIClient.axiosInstance.defaults.headers["Authorization"] = TokenHeader;
  }

  //Used to clear the access and refresh tokens, remove them from the authorization headers and add the refresh token to
  //the blacklist app
  public Logout(): Promise<boolean> {
    return APIClient.axiosInstance
      .post("/auth/logout", { refresh: localStorage.getItem("refresh_token") })
      .then((res) => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        APIClient.instance.SetAuthorizationHeaders(null);
        return true;
      });
  }

  //Used to create a new author from the create author component
  public PostAuthor(AuthorData: AuthorDetails): Promise<Number> {
    return APIClient.axiosInstance.post("/authors/", AuthorData).then((res) => {
      //Redirect to the details page of the currently created author
      const id: Number = res.data.id;
      return id;
    });
  }

  //Used to delete a given author from the delete author page
  public DeleteAuthor(id: string): Promise<Boolean> {
    return APIClient.axiosInstance
      .delete("/authors/" + id + "/")
      .then((res) => {
        return true;
      });
  }

  //Used to update a given authors data
  public PutAuthor(id: string, data: AuthorDetails): Promise<Boolean> {
    return APIClient.axiosInstance
      .put("/authors/" + id + "/", data)
      .then((res) => {
        return true;
      });
  }

  //Helper function for the axios interceptors.
  //Used to get a new access token using a refresh token
  private UseRefreshToken(refreshToken: string): Promise<string> {
    return APIClient.axiosInstance
      .post("/token/refresh/", { refresh: refreshToken })
      .then((response) => {
        const access_token: string = response.data.access;
        localStorage.setItem("access_token", access_token);
        APIClient.instance.SetAuthorizationHeaders("Bearer " + access_token);
        return access_token;
      });
  }
  //Used to intercept certain responses
  private getInterceptors() {
    APIClient.axiosInstance.interceptors.response.use(
      (response) => {
        //If the status code for the response is 2XX, do nothing and send the response forward
        return response;
      },
      (error) => {
        //If the status code is not 2XX
        //Process the request.
        const originalrequest = error.config;
        if (error.response) {
          if (error.response.status === 401 && !originalrequest._retry) {
            //If the status code is 401 and the request has not been retried before,
            //Check to see if the refresh token is valid
            originalrequest._retry = true;
            const refreshToken = localStorage.getItem("refresh_token");
            if (refreshToken != null) {
              const decoded_token: DecodedRefreshToken =
                jwt_decode(refreshToken);
              if (decoded_token.exp < Math.ceil(Date.now() / 1000)) {
                //if the refresh token is expired, logout the user and remove the access and refresh tokens,
                //redirect the user to the login page
                localStorage.removeItem("refresh_token");
                localStorage.removeItem("access_token");
                window.location.href = "/login/";
              }
              return APIClient.instance
                .UseRefreshToken(refreshToken)
                .then((access_token) => {
                  //If the refresh token is valid, generate a new access token and retry the original request
                  //with the new access token in the authorization header
                  originalrequest.headers["Authorization"] =
                    "Bearer " + access_token;
                  return APIClient.axiosInstance(originalrequest);
                });
            }
            //If the refresh token is not available, logout the user and redirect them to the login page
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("access_token");
            window.location.href = "/login/";
          }
          return Promise.reject(error);
        }
        return Promise.reject(error);
      }
    );
  }
}

export const client = APIClient.getInstance({
  /**
   * This is the axios instance used by the entire frontend app.
   * When a user logs in, the Authorization details are stored here so that all future requests use them.
   * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
   */
  timeout: 5000,
  headers: {
    Authorization: localStorage.getItem("access_token")
      ? localStorage.getItem("access_token")
      : null,
    "Content-Type": "application/json",
    accept: "application/json",
  },
  baseURL: "/",
  // transformResponse: [(response) =>{
  // 	return response.data
  // }]
});

const axiosInstance = axios.create({
  /**
   * This is the axios instance used by the entire frontend app.
   * When a user logs in, the Authorization details are stored here so that all future requests use them.
   * Axios interceptors will also be added to help with refreshing the access token and error handling in the future
   */
  timeout: 5000,
  headers: {
    Authorization: localStorage.getItem("access_token")
      ? localStorage.getItem("access_token")
      : null,
    "Content-Type": "application/json",
    accept: "application/json",
  },
  //baseURL: 'catalog/api/',
  // transformResponse: [(response) =>{
  // 	return response.data
  // }]
});

export default axiosInstance;
