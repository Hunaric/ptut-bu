import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridShapeComponent } from './grid-shape.component';

describe('GridShapeComponent', () => {
  let component: GridShapeComponent;
  let fixture: ComponentFixture<GridShapeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GridShapeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GridShapeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
