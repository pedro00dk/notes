#![allow(dead_code)]
use num::Num;
// use std::fmt::Debug;

pub trait Vx<T>
where
    Self: Copy,
    // Self: Index<usize, Output = T>, // + Index<Range<usize>, Output = [T]>
    // + Index<RangeFrom<usize>, Output = [T]>
    // + Index<RangeTo<usize>, Output = [T]>
    // + Index<RangeFull, Output = [T]>
    // + IndexMut<usize>
    // + IndexMut<Range<usize>>
    // + IndexMut<RangeFrom<usize>>
    // + IndexMut<RangeTo<usize>>
    // + IndexMut<RangeFull>,
    T: Copy,
{
    fn dim() -> usize;

    fn of(value: T) -> Self;
}

#[derive(Copy, Clone, Debug)]
pub struct V3<T> {
    pub x: T,
    pub y: T,
    pub z: T,
}

impl<T: Copy> Vx<T> for V3<T> {
    fn dim() -> usize {
        3
    }

    fn of(value: T) -> Self {
        Self {
            x: value,
            y: value,
            z: value,
        }
    }
}
