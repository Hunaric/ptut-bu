import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CrudBookComponent } from './crud-book.component';

describe('CrudBookComponent', () => {
  let component: CrudBookComponent;
  let fixture: ComponentFixture<CrudBookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CrudBookComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CrudBookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
