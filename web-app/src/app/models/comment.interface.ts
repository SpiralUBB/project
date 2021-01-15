export interface AppComment{
    id: string;
    text: string;
    author: Author;
    time: string;
}

export interface Author{
    firstName: string;
    lastName: string;
    points: number;
    trustLevel: number;
    username: string;
}
