import { TestBed } from '@angular/core/testing';

import { HttpResponseParserService } from './http-response-parser.service';

describe('HttpResponseParserService', () => {
  let service: HttpResponseParserService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HttpResponseParserService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
