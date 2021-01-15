export interface ApiResponse<T> {
  limit: number;
  no_items: number;
  no_pages: number;
  no_total_items: number;
  page: number;
  skip: number;
  items: T[];
}
